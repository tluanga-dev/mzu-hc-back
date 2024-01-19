from rest_framework import serializers
from .models import UnitOfMeasurement

class UnitOfMeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnitOfMeasurement
        fields = '__all__'