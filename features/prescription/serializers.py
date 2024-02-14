from rest_framework import serializers

from features.prescription.models import Prescription, PrescribedMedicine

class PrescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescription
        fields = "__all__"

class PrescriptionItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrescribedMedicine
        fields = "__all__"