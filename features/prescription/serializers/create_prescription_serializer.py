from datetime import datetime
import logging
from rest_framework import serializers
from django.db import transaction
from django.utils.dateparse import parse_datetime
from features.item.models import Item
from features.patient.models import Patient
from features.person.models import MZUOutsider, Student, Employee, EmployeeDependent
from features.prescription.models import Prescription, PrescriptionItem
from features.medicine.models import MedicineDosage, MedicineDosageTiming
from features.patient.serializers import PatientSerializer
from features.person.serializers import MZUOutsiderSerializer
from features.prescription.serializers.prescription_serializer import PrescriptionDetailSerializer

logger = logging.getLogger('features.prescription')  # Ensure this matches the name used in settings.py


class CreatePrescriptionSerializer(serializers.Serializer):
    patient_type = serializers.ChoiceField(choices=Patient.PatientType.choices)
    # patient_data = PatientSerializer()
    patient_data = serializers.JSONField() 
    prescription_data = serializers.JSONField()  # We'll manually handle nested validation
    mzu_outsider_data = MZUOutsiderSerializer(required=False)

    def validate(self, attrs):
        try:
            logger.debug("Starting validation")
            print('validate method called')
            patient_type = attrs.get('patient_type')
            mzu_outsider_data = attrs.get('mzu_outsider_data')

            if patient_type == Patient.PatientType.MZU_OUTSIDER and not mzu_outsider_data:
                logger.error("Validation failed: MZUOutsider data is required for 'MZU_outsider' patient type.")
                raise serializers.ValidationError("MZUOutsider data is required for 'MZU_outsider' patient type.")
            
            logger.debug("Validation successful")
            return attrs
        except:
            logger.exception("Validation failed")
            raise serializers.ValidationError("Validation failed")

    def create(self, validated_data):
        logger.debug("Starting creation process")
        print('create method called')
        patient_type = validated_data.get('patient_type')
        patient_data = validated_data.get('patient_data')
        prescription_data = validated_data.get('prescription_data')
        mzu_outsider_data = validated_data.get('mzu_outsider_data', None)

        try:
            with transaction.atomic():
                print('Starting patient creation or retrieval process')
                logger.debug("Starting patient creation or retrieval process")
                # Create or get patient based on patient_type
                if patient_type == Patient.PatientType.EMPLOYEE:
                    if isinstance(patient_data['employee'], Employee):
                        patient_data['employee'] = patient_data['employee'].pk
                    patient_data.pop('id', None)  # Remove the 'id' field
                    employee, created = Employee.objects.get_or_create(pk=patient_data.pop('employee'))
                    patient, created = Patient.objects.get_or_create(employee=employee, defaults=patient_data)               
                elif patient_type == Patient.PatientType.STUDENT:
                    logger.debug("Processing patient type: STUDENT")
                    if isinstance(patient_data['student'], Student):
                        patient_data['student'] = patient_data['student'].pk
                    student = Student.objects.select_for_update().get(pk=patient_data.pop('student'))
                    patient, created = Patient.objects.get_or_create(student=student, defaults=patient_data)
                elif patient_type == Patient.PatientType.EMPLOYEE_DEPENDENT:
                    logger.debug("Processing patient type: EMPLOYEE_DEPENDENT")
                    if isinstance(patient_data['employee_dependent'], EmployeeDependent):
                        patient_data['employee_dependent'] = patient_data['employee_dependent'].pk
                    employee_dependent = EmployeeDependent.objects.select_for_update().get(pk=patient_data.pop('employee_dependent'))
                    patient, created = Patient.objects.get_or_create(employee_dependent=employee_dependent, defaults=patient_data)
                elif patient_type == Patient.PatientType.MZU_OUTSIDER:
                    logger.debug("Processing patient type: MZU_OUTSIDER")
                    mzu_outsider_patient = MZUOutsider.objects.create(**mzu_outsider_data)
                    patient, created = Patient.objects.get_or_create(mzu_outsider=mzu_outsider_patient, defaults=patient_data)
                else:
                    logger.error("Invalid patient type or missing MZUOutsider data")
                    raise serializers.ValidationError("Invalid patient type or missing MZUOutsider data")

                logger.debug("Patient creation or retrieval successful")

                # Convert date and time to a datetime object
                date_and_time_str = prescription_data.pop('date_and_time')
                print('date and time:', date_and_time_str)
                parsed_date = datetime.strptime(date_and_time_str, "%d-%m-%Y %H:%M:%S")
                print('parsed date and time:', parsed_date)
                if parsed_date is None:
                    logger.error("Invalid date and time format")
                    raise serializers.ValidationError("Invalid date and time format.")

                logger.debug("Date and time parsed successfully")

                # Create prescription with the associated patient
                prescription_data['patient'] = patient  # Assign the Patient instance, not the UUID
                prescription_data['date_and_time'] = parsed_date  # Assign the converted datetime object

                prescribed_item_set_data = prescription_data.pop('prescribed_item_set', [])

                logger.debug("Creating prescription")
                # Save the prescription first
                new_prescription = Prescription.objects.create(**prescription_data)

                new_prescription.save()  # Ensure the prescription is saved and its ID is generated
                print('new prescription:',new_prescription.id)
                def create_prescription_items():
                    if new_prescription:
                        for prescribed_item_data in prescribed_item_set_data:
                            medicine_id = prescribed_item_data.pop('medicine')
                            try:
                                medicine = Item.objects.select_for_update().get(id=medicine_id)
                            except Item.DoesNotExist:
                                raise serializers.ValidationError(f"Medicine with ID {medicine_id} does not exist.")
                            medicine_dosage_list_data = prescribed_item_data.pop('dosages', [])
                            prescription_item = PrescriptionItem.objects.create(prescription=new_prescription, medicine=medicine)

                            for medicine_dosage_data in medicine_dosage_list_data:
                                medicine_dosage_timing_set_data = medicine_dosage_data.pop('medicine_dosage_timing_set', [])
                                medicine_dosage = MedicineDosage.objects.create(**medicine_dosage_data, medicine=medicine)
                                prescription_item.dosages.add(medicine_dosage)

                                for medicine_dosage_timing_data in medicine_dosage_timing_set_data:
                                    MedicineDosageTiming.objects.create(**medicine_dosage_timing_data, medicine_dosage=medicine_dosage)

                # Ensure prescription items are created only after the prescription is committed
                transaction.on_commit(create_prescription_items)

                logger.debug("Prescription item creation successful")
            return {
                'patient': PatientSerializer(patient).data,
                'prescription': PrescriptionDetailSerializer(new_prescription).data
            }

        except Exception as e:
            logger.exception('Exception: %s', e)
            import traceback
            traceback.print_exc()
            raise serializers.ValidationError(f"Validation Error occurred: {str(e)}")
