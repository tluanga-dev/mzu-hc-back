from rest_framework import serializers
from features.prescription.models import Prescription, PrescriptionItem
from features.patient.serializers import PatientSerializer
from features.prescription.serializers.prescription_item_serializer import PrescriptionItemSerializer

class PrescriptionSerializer(serializers.ModelSerializer):
    prescribed_item_set = PrescriptionItemSerializer(many=True)
    date_and_time = serializers.DateTimeField(format="%d-%m-%Y %H:%M:%S")

    class Meta:
        model = Prescription
        fields = [
            'id',
            'code', 
            'patient', 
            'chief_complaints',
            'diagnosis',
            'advice_and_instructions', 
            'date_and_time', 
            'prescription_dispense_status', 
            'prescribed_item_set'
        ]
        read_only_fields = ['code']

    def create(self, validated_data):
        prescribed_item_set_data = validated_data.pop('prescribed_item_set')
        prescription = Prescription.objects.create(**validated_data)
        for item_data in prescribed_item_set_data:
            PrescriptionItem.objects.create(prescription=prescription, **item_data)
        return prescription

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['patient'] = PatientSerializer(instance.patient).data
        return representation
