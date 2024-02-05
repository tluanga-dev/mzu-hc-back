# serializers.py

from rest_framework import serializers
from .models import Item, ItemBatch, ItemCategory, ItemType, UnitOfMeasurement

class UnitOfMeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnitOfMeasurement
        fields = '__all__'

class ItemCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemCategory
        fields = ['id', 'name', 'abbreviation', 'description', 'is_active', 'created_on', 'updated_on']


class ItemTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemType
        fields = ['id', 'name', 'abbreviation', 'description', 'example', 'category', 'is_active', 'created_on', 'updated_on']

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'name', 'description', 'type', 'is_active', 'created_on', 'updated_on']

class ItemBatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemBatch
        fields = ['batch_id', 'description', 'date_of_expiry', 'item', 'is_active', 'created_on', 'updated_on']