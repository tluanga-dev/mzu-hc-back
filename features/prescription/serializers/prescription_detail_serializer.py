from rest_framework import serializers
from features.prescription.models import Prescription, PrescriptionItem
from features.prescription.serializers.prescription_item_serializer import PrescriptionItemSerializer



class PrescriptionDetailSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    code = serializers.CharField(read_only=True)
    patient = serializers.SerializerMethodField()
    chief_complaints = serializers.CharField()
    diagnosis = serializers.CharField()
    advice_and_instructions = serializers.CharField()
    date_and_time = serializers.DateTimeField(format="%d-%m-%Y %H:%M:%S")
    prescription_dispense_status = serializers.CharField()
    prescribed_item_set = PrescriptionItemSerializer(many=True)

    def get_patient(self, instance):
        return {
            'id': instance.patient.id,
            'name': instance.patient.get_name(),
            'patient_type': instance.patient.patient_type,
            'mzu_id': instance.patient.get_mzu_id(),
            'age': instance.patient.get_age(),
            'gender':instance.patient.get_gender(),
            'organisation_unit': instance.patient.get_organisation_unit()
        }

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['patient'] = self.get_patient(instance)
        return representation
