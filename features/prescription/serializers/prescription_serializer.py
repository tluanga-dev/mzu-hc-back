from rest_framework import serializers
from features.prescription.models import Prescription, PrescriptionItem
from features.patient.serializers import PatientSerializer
from features.prescription.serializers.prescription_detail_serializer import PrescriptionDetailSerializer
from features.prescription.serializers.prescription_item_serializer import PrescriptionItemSerializer

from rest_framework import serializers
from django.db import transaction
from features.patient.models import Patient
from features.person.models import MZUOutsider, Student, Employee, EmployeeDependent
from features.prescription.models import Prescription, PrescriptionItem
from features.medicine.models import MedicineDosage, MedicineDosageTiming
from features.patient.serializers import PatientSerializer
from features.person.serializers import MZUOutsiderSerializer
from features.prescription.serializers.prescription_item_serializer import PrescriptionItemSerializer

class PrescriptionListSerializer(serializers.ModelSerializer):
    date_and_time = serializers.DateTimeField(format="%d-%m-%Y %H:%M:%S")

    class Meta:
        model = Prescription
        fields = [
            'id',
            'code', 
            'date_and_time', 
            'prescription_dispense_status'
        ]
        read_only_fields = ['code']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # representation['patient'] = {
        #     'id':instance.patient.id,
        #     'name': instance.patient.get_name(),
        #     'patient_type': instance.patient.patient_type,
        #     'mzu_id': instance.patient.get_mzu_id()
        # } 
        representation['patient_name']=instance.patient.get_name()
        return representation


class PrescriptionSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    code = serializers.CharField(read_only=True)
    patient_type = serializers.ChoiceField(choices=Patient.PatientType.choices, write_only=True)
    patient_data = PatientSerializer(write_only=True)
    mzu_outsider_data = MZUOutsiderSerializer(required=False, write_only=True)
    patient = serializers.SerializerMethodField(read_only=True)
    chief_complaints = serializers.CharField()
    diagnosis = serializers.CharField()
    advice_and_instructions = serializers.CharField()
    date_and_time = serializers.DateTimeField(format="%d-%m-%Y %H:%M:%S")
    prescription_dispense_status = serializers.CharField()
    prescribed_item_set = PrescriptionItemSerializer(many=True)


    def validate(self, attrs):
        patient_type = attrs.get('patient_type')
        mzu_outsider_data = attrs.get('mzu_outsider_data')

        if patient_type == 'Other' and not mzu_outsider_data:
            raise serializers.ValidationError("MZUOutsider data is required for 'Other' patient type.")
        return attrs

    def get_patient(self, instance):
       
        return {
            'id': instance.patient.id,
            'name': instance.patient.get_name(),
            'patient_type': instance.patient.patient_type,
            'gender':instance.patient.get_gender(),
            'mzu_id': instance.patient.get_mzu_id(),
            'age': instance.patient.get_age(),
            'organisation_unit': instance.patient.get_organisation_unit()
        }

    @transaction.atomic
    def update(self, instance, validated_data):
        patient_type = validated_data.get('patient_type')
        patient_data = validated_data.get('patient_data')
        prescription_data = validated_data
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
                'prescription': PrescriptionDetailSerializer(instance).data
            }

        except Exception as e:
            raise serializers.ValidationError(f"Error occurred: {str(e)}")

    def to_representation(self, instance):
        print('instnace',instance)
        print(instance.prescribed_item_set)
        representation = super().to_representation(instance)
        representation['patient'] = self.get_patient(instance)
        representation['prescribed_item_set'] = PrescriptionItemSerializer(instance.prescribed_item_set.all(), many=True).data
        return representation
