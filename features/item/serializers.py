# serializers.py

from rest_framework import serializers

from features.inventory_transaction.inventory_transaction.models import ItemStockInfo
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
                  'is_active', 'created_at', 'updated_at']


class ItemCategorySerializerForUser(serializers.ModelSerializer):
    class Meta:
        model = ItemCategory
        fields = ['id', 'name', 'abbreviation', 'description']


class ItemTypeSerializer(serializers.ModelSerializer):
    category = ItemCategorySerializerForUser(read_only=True)

    class Meta:
        model = ItemType
        fields = ['id', 'name', 'abbreviation', 'description',
                  'example', 'category', 'is_active', 'created_at', 'updated_at']


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
                  'is_active', 'created_at', 'updated_at']


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
                  'item', 'is_active', 'created_at', 'updated_at']
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


class ItemWithStockInfoSerializer(serializers.ModelSerializer):

    quantity_in_stock = serializers.IntegerField(read_only=True)
    category = serializers.CharField(read_only=True)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        item_stock_info = ItemStockInfo.get_latest_by_item_id(instance.id)
        quantity_in_stock = item_stock_info.item_quantity_in_stock if item_stock_info else 0
        representation['type']=instance.type.name
        representation['category']=instance.type.category.name
        representation['quantity_in_stock'] = quantity_in_stock
        representation['unit_of_measurement']=UnitOfMeasurementSerializerForUser(instance.unit_of_measurement).data["name"]
    
        return representation

    class Meta:
        model = Item
        fields = [
            'id',
            'name', 
            'description', 
            'type', 
            'category',
            'unit_of_measurement',
            'quantity_in_stock'
        ]

class ItemDetailSerializerForReport(serializers.ModelSerializer):
    type = ItemTypeSerializerForUser(read_only=True)
    item_batches = ItemBatchSerializer(many=True, read_only=True)
    unit_of_measurement = UnitOfMeasurementSerializerForUser(read_only=True)
    quantity_in_stock = serializers.IntegerField(read_only=True)

    # ---- get all the 


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        item_stock_info = ItemStockInfo.get_latest_by_item_id(instance.id)
        quantity_in_stock = item_stock_info.item_quantity_in_stock if item_stock_info else 0
        representation['quantity_in_stock'] = quantity_in_stock
   
    
        return representation

    class Meta:
        model = Item
        fields = ['id', 'name', 'description', 'type', 'unit_of_measurement','item_batches','quantity_in_stock']