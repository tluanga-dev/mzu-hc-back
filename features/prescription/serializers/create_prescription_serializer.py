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
from features.prescription.serializers.prescription_serializer import PrescriptionSerializer

# Configure logging
logger = logging.getLogger(__name__)

class CreatePrescriptionSerializer(serializers.Serializer):
    patient_type = serializers.ChoiceField(choices=Patient.PatientType.choices)
    patient_data = PatientSerializer()
    prescription_data = serializers.JSONField()  # We'll manually handle nested validation
    mzu_outsider_data = MZUOutsiderSerializer(required=False)

    def validate(self, attrs):
        patient_type = attrs.get('patient_type')
        mzu_outsider_data = attrs.get('mzu_outsider_data')

        if patient_type == Patient.PatientType.MZU_OUTSIDER and not mzu_outsider_data:
            raise serializers.ValidationError("MZUOutsider data is required for 'MZU_outsider' patient type.")
        
        return attrs

    def create(self, validated_data):
        patient_type = validated_data.get('patient_type')
        patient_data = validated_data.get('patient_data')
        prescription_data = validated_data.get('prescription_data')
        mzu_outsider_data = validated_data.get('mzu_outsider_data', None)

        try:
            with transaction.atomic():
                # Create or get patient based on patient_type
                if patient_type == Patient.PatientType.EMPLOYEE:
                    if isinstance(patient_data['employee'], Employee):
                        patient_data['employee'] = patient_data['employee'].pk
                    employee = Employee.objects.select_for_update().get(pk=patient_data.pop('employee'))
                    patient, created = Patient.objects.get_or_create(employee=employee, defaults=patient_data)
                elif patient_type == Patient.PatientType.STUDENT:
                    if isinstance(patient_data['student'], Student):
                        patient_data['student'] = patient_data['student'].pk
                    student = Student.objects.select_for_update().get(pk=patient_data.pop('student'))
                    patient, created = Patient.objects.get_or_create(student=student, defaults=patient_data)
                elif patient_type == Patient.PatientType.EMPLOYEE_DEPENDENT:
                    if isinstance(patient_data['employee_dependent'], EmployeeDependent):
                        patient_data['employee_dependent'] = patient_data['employee_dependent'].pk
                    employee_dependent = EmployeeDependent.objects.select_for_update().get(pk=patient_data.pop('employee_dependent'))
                    patient, created = Patient.objects.get_or_create(employee_dependent=employee_dependent, defaults=patient_data)
                elif patient_type == Patient.PatientType.MZU_OUTSIDER:
                    mzu_outsider_patient = MZUOutsider.objects.create(**mzu_outsider_data)
                    patient, created = Patient.objects.get_or_create(mzu_outsider=mzu_outsider_patient, defaults=patient_data)
                else:
                    raise serializers.ValidationError("Invalid patient type or missing MZUOutsider data")

                # Convert date and time to a datetime object
                date_and_time_str = prescription_data.pop('date_and_time')
                date_and_time = parse_datetime(date_and_time_str)
                if date_and_time is None:
                    raise serializers.ValidationError("Invalid date and time format.")

                # Create prescription with the associated patient
                prescription_data['patient'] = patient  # Assign the Patient instance, not the UUID
                prescription_data['date_and_time'] = date_and_time  # Assign the converted datetime object

                prescribed_item_set_data = prescription_data.pop('prescribed_item_set', [])

                # Save the prescription first
                new_prescription = Prescription.objects.create(**prescription_data)
                new_prescription.save()  # Ensure the prescription is saved and its ID is generated

                def create_prescription_items():
                    if new_prescription:
                        for prescribed_item_data in prescribed_item_set_data:
                            medicine_id = prescribed_item_data.pop('medicine')
                            medicine = Item.objects.select_for_update().get(id=medicine_id)
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

            return {
                'patient': PatientSerializer(patient).data,
                'prescription': PrescriptionSerializer(new_prescription).data
            }

        except Exception as e:
            logger.exception('Exception: %s', e)
            raise serializers.ValidationError(f"Error occurred: {str(e)}")
