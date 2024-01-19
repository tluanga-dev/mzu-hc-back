# serializers.py

from rest_framework import serializers
from .models import ItemType

class ItemTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemType
        fields = ['id', 'name', 'abbreviation', 'description', 'example', 'category', 'is_active', 'created_on', 'updated_on']