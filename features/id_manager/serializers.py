from rest_framework import serializers
from .models import IdManager

class IdManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = IdManager
        fields = ['id', 'name', 'description', 'latest_id', 'is_active', 'created_at', 'updated_at']