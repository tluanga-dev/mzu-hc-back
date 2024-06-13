from rest_framework import serializers

from features.item.models import UnitOfMeasurement

class UnitOfMeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnitOfMeasurement
        fields = '__all__'


class UnitOfMeasurementSerializerForUser(serializers.ModelSerializer):
  
    class Meta:
        model = UnitOfMeasurement
        fields = ['id', 'name', 'abbreviation', 'description']