from datetime import datetime
import logging
from rest_framework import serializers
from django.db import transaction
from features.item.models import Item
from features.patient.models import Patient
from features.person.models import MZUOutsider, Student, Employee, EmployeeDependent
from features.prescription.models import Prescription, PrescriptionItem
from features.medicine.models import MedicineDosage, MedicineDosageTiming
from features.person.serializers import MZUOutsiderSerializer
from features.prescription.serializers.prescription_item_serializer import PrescriptionItemSerializer

logger = logging.getLogger('features.prescription')

class CreatePrescriptionSerializer(serializers.Serializer):
    patient_type = serializers.ChoiceField(choices=Patient.PatientType.choices)
    patient_data = serializers.JSONField()
    prescription_data = serializers.JSONField()
    mzu_outsider_data = MZUOutsiderSerializer(required=False)

    def validate(self, attrs):
        try:
            logger.debug("Starting validation")
            patient_type = attrs.get('patient_type')
            mzu_outsider_data = attrs.get('mzu_outsider_data')

            if patient_type == Patient.PatientType.MZU_OUTSIDER and not mzu_outsider_data:
                logger.error("Validation failed: MZUOutsider data is required for 'MZU_outsider' patient type.")
                raise serializers.ValidationError("MZUOutsider data is required for 'MZU_outsider' patient type.")
            
            logger.debug("Validation successful")
            return attrs
        except Exception as e:
            logger.exception("Validation failed: %s", e)
            raise serializers.ValidationError("Validation failed")

    def create(self, validated_data):
        logger.debug("Starting creation process")
        patient_type = validated_data.get('patient_type')
        patient_data = validated_data.get('patient_data')
        prescription_data = validated_data.get('prescription_data')
        mzu_outsider_data = validated_data.get('mzu_outsider_data', None)
        age=0; 
        try:
            with transaction.atomic():
                logger.debug("Starting patient creation or retrieval process")
                if patient_type == Patient.PatientType.EMPLOYEE:
                    if isinstance(patient_data['employee'], Employee):
                        patient_data['employee'] = patient_data['employee'].pk
                    patient_data.pop('id', None)
                    employee, created = Employee.objects.get_or_create(pk=patient_data.pop('employee'))
                    patient, created = Patient.objects.get_or_create(employee=employee, defaults=patient_data)               
                    patient_data=Patient.objects.select_for_update().get(id=patient.id)
                    age=patient_data.employee.get_age()
                elif patient_type == Patient.PatientType.STUDENT:
                    if isinstance(patient_data['student'], Student):
                        patient_data['student'] = patient_data['student'].pk
                    student = Student.objects.select_for_update().get(pk=patient_data.pop('student'))
                    patient, created = Patient.objects.get_or_create(student=student, defaults=patient_data)
                    patient_data=Patient.objects.select_for_update().get(id=patient.id)
                elif patient_type == Patient.PatientType.EMPLOYEE_DEPENDENT:
                    if isinstance(patient_data['employee_dependent'], EmployeeDependent):
                        patient_data['employee_dependent'] = patient_data['employee_dependent'].pk
                    employee_dependent = EmployeeDependent.objects.select_for_update().get(pk=patient_data.pop('employee_dependent'))
                    patient, created = Patient.objects.get_or_create(employee_dependent=employee_dependent, defaults=patient_data)
                    patient_data=Patient.objects.select_for_update().get(id=patient.id)
                elif patient_type == Patient.PatientType.MZU_OUTSIDER:
                    mzu_outsider_patient = MZUOutsider.objects.create(**mzu_outsider_data)
                    patient, created = Patient.objects.get_or_create(mzu_outsider=mzu_outsider_patient, defaults=patient_data)
                    patient_data=Patient.objects.select_for_update().get(id=patient.id)
                else:
                    logger.error("Invalid patient type or missing MZUOutsider data")
                    raise serializers.ValidationError("Invalid patient type or missing MZUOutsider data")

                logger.debug("Patient creation or retrieval successful")

                date_and_time_str = prescription_data.pop('date_and_time')
                parsed_date = datetime.strptime(date_and_time_str, "%d-%m-%Y %H:%M:%S")
                if parsed_date is None:
                    logger.error("Invalid date and time format")
                    raise serializers.ValidationError("Invalid date and time format.")

                logger.debug("Date and time parsed successfully")

                prescription_data['patient'] = patient
                prescription_data['date_and_time'] = parsed_date

                prescribed_item_set_data = prescription_data.pop('prescribed_item_set', [])

                logger.debug("Creating prescription")
         
                new_prescription = Prescription.objects.create(
                    **prescription_data
                )
               
                data=Prescription.objects.all()
                print('data',data)
                


                MZUOutsider.objects.create(name='thanga', age=24, gender='Male')

                # Function to create prescription items
            def create_prescription_items(prescription_id):
                    for prescribed_item_data in prescribed_item_set_data:
                        medicine_id = prescribed_item_data.pop('medicine')
                        try:
                            medicine = Item.objects.get(id=medicine_id)
                        except Item.DoesNotExist:
                            raise serializers.ValidationError(f"Medicine with ID {medicine_id} does not exist.")
                        medicine_dosage_list_data = prescribed_item_data.pop('dosages', [])
                        prescription_item = PrescriptionItem.objects.create(prescription_id=prescription_id, medicine=medicine)

                        for medicine_dosage_data in medicine_dosage_list_data:
                            medicine_dosage_timing_set_data = medicine_dosage_data.pop('medicine_dosage_timing_set', [])
                            medicine_dosage = MedicineDosage.objects.create(**medicine_dosage_data, medicine=medicine)
                            prescription_item.dosages.add(medicine_dosage)

                            for medicine_dosage_timing_data in medicine_dosage_timing_set_data:
                                MedicineDosageTiming.objects.create(**medicine_dosage_timing_data, medicine_dosage=medicine_dosage)

                # Ensure prescription items are created only after the prescription is committed
            transaction.on_commit(lambda: create_prescription_items(new_prescription.id))

            logger.debug("Prescription item creation scheduled")
                
            returnable= {
                'id': new_prescription.id,
                'code': new_prescription.code,
                'chief_complaints':new_prescription.chief_complaints,
                'diagnosis':new_prescription.diagnosis,
                'advice_and_instructions':new_prescription.advice_and_instructions,
                'date_and_time':new_prescription.date_and_time,
                'prescription_dispense_status':new_prescription.prescription_dispense_status,
                'prescribed_item_set': PrescriptionItemSerializer(new_prescription.prescribed_item_set, many=True).data,

                'patient': {
                    'patient_type': patient_type,
                    'id': patient_data.id,
                    'name': patient_data.employee.get_name() if patient_data.employee else patient_data.student.get_name() if patient_data.student else patient_data.employee_dependent.get_name() if patient_data.employee_dependent else patient_data.mzu_outsider.get_name() if patient_data.mzu_outsider else '',
                    'mzu_id': patient_data.employee.get_mzu_employee_id() if patient_data.employee else patient_data.student.mzu_student_id if patient_data.student else patient_data.employee_dependent.mzu_employee_dependent_id if patient_data.employee_dependent else '',
                    'age':age,
                    'organisation_unit': patient_data.employee.organisation_unit.name if patient_data.employee else patient_data.student.organisation_unit.name if patient_data.student else '',
                    # 'date_of_birth': patient_data.date_of_birth,
                    # 'age': patient_data.age,
                    
                },
                
            }
            print(returnable)
            return returnable

        except Exception as e:
            logger.exception('Exception: %s', e)
            raise serializers.ValidationError(f"Validation Error occurred: {str(e)}")
