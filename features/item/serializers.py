# serializers.py

from rest_framework import serializers

from features.utils.convert_date import DateConverter
from .models import Item, ItemBatch, ItemCategory, ItemType, UnitOfMeasurement

class UnitOfMeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnitOfMeasurement
        fields = '__all__'

class ItemCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemCategory
        fields = ['id', 'name', 'abbreviation', 'description', 'is_active', 'created_on', 'updated_on']


class ItemCategorySerializerForUser(serializers.ModelSerializer):
    class Meta:
        model = ItemCategory
        fields = ['id', 'name', 'abbreviation', 'description']


class ItemTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ItemType
        fields = ['id', 'name', 'abbreviation', 'description', 'example', 'category', 'is_active', 'created_on', 'updated_on']

class ItemTypeSerializerForUser(serializers.ModelSerializer):
    category=ItemCategorySerializerForUser(read_only=True)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['category'] = ItemCategorySerializerForUser(instance.category).data
        return representation
    class Meta:
        model = ItemType
        fields = ['id', 'name', 'abbreviation', 'description', 'example', 'category']




class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = ['id', 'name', 'description', 'type', 'is_active', 'created_on', 'updated_on']


class CustomDateField(serializers.DateField):
    def to_representation(self, value):
        return value.strftime("%d-%m-%Y")

class ItemBatchSerializer(serializers.ModelSerializer):
    date_of_expiry = CustomDateField()

    def to_internal_value(self, data):
        # Convert the incoming date_and_time to the database format
        
        if 'date_of_expiry' in data:
            try:
                converted_date_and_time= DateConverter.convert_date_format_to_django_default(
                    data['date_of_expiry']
                ) 
                
                data['date_of_expiry'] =converted_date_and_time
            except ValueError:
                raise serializers.ValidationError({"date_of_expiry": "Date of expiry must be in 'dd-mm-yyyy hh:mm' format"})
        return super().to_internal_value(data)


    class Meta:
        model = ItemBatch
        fields = ['batch_id', 'description', 'date_of_expiry', 'item', 'is_active', 'created_on', 'updated_on']



class ItemSerializerForUser(serializers.ModelSerializer):
    
    type=ItemTypeSerializerForUser(read_only=True)
    item_batches=ItemBatchSerializer(many=True, read_only=True)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['type'] = ItemTypeSerializerForUser(instance.type).data
        
        return representation
    
    class Meta:
        model = Item
        fields = ['id', 'name', 'description', 'type', 'item_batches']

