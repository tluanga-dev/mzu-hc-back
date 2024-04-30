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
        fields = ['id', 'name', 'abbreviation', 'description',
                  'is_active', 'created_on', 'updated_on']


class ItemCategorySerializerForUser(serializers.ModelSerializer):
    class Meta:
        model = ItemCategory
        fields = ['id', 'name', 'abbreviation', 'description']


class ItemTypeSerializer(serializers.ModelSerializer):
    category = ItemCategorySerializerForUser(read_only=True)

    class Meta:
        model = ItemType
        fields = ['id', 'name', 'abbreviation', 'description',
                  'example', 'category', 'is_active', 'created_on', 'updated_on']


class ItemTypeSerializerForUser(serializers.ModelSerializer):
    category = ItemCategorySerializerForUser(read_only=True)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['category'] = ItemCategorySerializerForUser(
            instance.category).data
        return representation

    class Meta:
        model = ItemType
        fields = ['id', 'name', 'abbreviation',
                  'description', 'example', 'category']


class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = ['id', 'name', 'description', 'type',
                  'is_active', 'created_on', 'updated_on']


class CustomDateField(serializers.DateField):
    def to_representation(self, value):
        try:
            value = value.strftime("%d-%m-%Y")
            return value
        except ValueError as e:
            print('There is an error- ', e)

    def to_internal_value(self, data):
        return DateConverter.convert_date_format(data)


class ItemBatchSerializer(serializers.ModelSerializer):
    date_of_expiry = CustomDateField()

    class Meta:
        model = ItemBatch
        fields = ['id', 'batch_id', 'description', 'date_of_expiry',
                  'item', 'is_active', 'created_on', 'updated_on']
class UnitOfMeasurementSerializerForUser(serializers.ModelSerializer):
  
    class Meta:
        model = UnitOfMeasurement
        fields = ['id', 'name', 'abbreviation', 'description']

class ItemSerializerForUser(serializers.ModelSerializer):

    type = ItemTypeSerializerForUser(read_only=True)
    item_batches = ItemBatchSerializer(many=True, read_only=True)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['type'] = ItemTypeSerializerForUser(instance.type).data
        representation['unit_of_measurement']=UnitOfMeasurementSerializerForUser(instance.unit_of_measurement).data

        return representation

    class Meta:
        model = Item
        fields = ['id', 'name','contents', 'description', 'type', 'item_batches','unit_of_measurement']


class ItemWithStockInfoSerializer(ItemSerializerForUser):
    item_batches = ItemBatchSerializer(many=True, read_only=True)
    quantity_in_stock = serializers.IntegerField(read_only=True)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['quantity_in_stock'] = 0
        return representation

    class Meta:
        model = Item
        fields = [
            'id',
            'name', 
            'description', 
            'type', 
            'item_batches',
            'quantity_in_stock'
        ]