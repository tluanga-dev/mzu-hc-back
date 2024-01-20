# serializers.py

from rest_framework import serializers
from .models import MedicineDosageDuration

class MedicineDosageDurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicineDosageDuration
        fields = ['id', 'days', 'name', 'updated_on']