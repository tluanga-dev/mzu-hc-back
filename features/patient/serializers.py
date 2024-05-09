from rest_framework import serializers

from features.patient.models import Patient


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model=Patient
        fields='__all__'
        read_only_fields = ['mzu_hc_id']

