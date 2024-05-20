from rest_framework import serializers
from django.db import transaction
from features.patient.models import Patient
from features.person.models import MZUOutsider, Student, Employee, EmployeeDependent
from features.prescription.models import Prescription, PrescriptionItem
from features.medicine.models import MedicineDosage, MedicineDosageTiming
from features.patient.serializers import PatientSerializer
from features.person.serializers import MZUOutsiderSerializer
from features.prescription.serializers.prescription_serializer import PrescriptionSerializer


class UpdatePrescriptionSerializer(serializers.Serializer):
    patient_type = serializers.ChoiceField(choices=Patient.PATIENT_TYPE_CHOICES)
    patient_data = PatientSerializer()
    prescription_data = serializers.JSONField()  # We'll manually handle nested validation
    mzu_outsider_data = MZUOutsiderSerializer(required=False)

    def validate(self, attrs):
        patient_type = attrs.get('patient_type')
        mzu_outsider_data = attrs.get('mzu_outsider_data')

        if patient_type == 'Other' and not mzu_outsider_data:
            raise serializers.ValidationError("MZUOutsider data is required for 'Other' patient type.")
        
        return attrs

    @transaction.atomic
    def update(self, instance, validated_data):
        patient_type = validated_data.get('patient_type')
        patient_data = validated_data.get('patient_data')
        prescription_data = validated_data.get('prescription_data')
        mzu_outsider_data = validated_data.get('mzu_outsider_data', None)

        try:
            # Update or get patient based on patient_type
            if patient_type == 'Employee':
                employee = Employee.objects.get(pk=patient_data.pop('employee'))
                patient, created = Patient.objects.update_or_create(employee=employee, defaults=patient_data)
            elif patient_type == 'Student':
                student = Student.objects.get(pk=patient_data.pop('student'))
                patient, created = Patient.objects.update_or_create(student=student, defaults=patient_data)
            elif patient_type == 'Employee Dependent':
                employee_dependent = EmployeeDependent.objects.get(pk=patient_data.pop('employee_dependent'))
                patient, created = Patient.objects.update_or_create(employee_dependent=employee_dependent, defaults=patient_data)
            elif patient_type == 'Other':
                mzu_outsider_patient = MZUOutsider.objects.create(**mzu_outsider_data)
                patient, created = Patient.objects.update_or_create(mzu_outsider_patient=mzu_outsider_patient, defaults=patient_data)
            else:
                raise serializers.ValidationError("Invalid patient type or missing MZUOutsider data")

            # Update prescription with the associated patient
            prescription_data['patient'] = patient.id

            # Handle prescribed items and nested dosages
            prescribed_item_set_data = prescription_data.pop('prescribed_item_set', [])
            
            # Update the prescription instance
            for attr, value in prescription_data.items():
                setattr(instance, attr, value)
            instance.save()

            # Clear existing prescribed items
            instance.prescribed_item_set.all().delete()

            # Re-create prescribed items
            for prescribed_item_data in prescribed_item_set_data:
                medicine_dosage_list_data = prescribed_item_data.pop('dosages', [])
                prescription_item = PrescriptionItem.objects.create(**prescribed_item_data, prescription=instance)
                medicine = prescription_item.medicine

                for medicine_dosage_data in medicine_dosage_list_data:
                    medicine_dosage_timing_set_data = medicine_dosage_data.pop('medicine_dosage_timing_set', [])
                    medicine_dosage = MedicineDosage.objects.create(**medicine_dosage_data, medicine=medicine)
                    prescription_item.dosages.add(medicine_dosage)

                    for medicine_dosage_timing_data in medicine_dosage_timing_set_data:
                        MedicineDosageTiming.objects.create(**medicine_dosage_timing_data, medicine_dosage=medicine_dosage)

            return {
                'patient': PatientSerializer(patient).data,
                'prescription': PrescriptionSerializer(instance).data
            }

        except Exception as e:
            raise serializers.ValidationError(f"Error occurred: {str(e)}")
