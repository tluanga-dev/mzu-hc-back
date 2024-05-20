from rest_framework import serializers
from features.prescription.models import Prescription
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

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['patient'] = PatientSerializer(instance.patient).data
        # representation['doctor'] = PrescriptionPersonSerializer(instance.doctor).data
        return representation