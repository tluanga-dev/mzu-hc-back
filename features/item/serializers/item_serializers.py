from rest_framework import serializers
from features.inventory_transaction.inventory_transaction.models import ItemStockInfo
from features.item.models import Item, MedicineDosageUnit
from features.item.serializers.item_batch_serializers import ItemBatchSerializer
from features.item.serializers.item_packaging_serialzers import ItemPackagingSerializer
from features.item.serializers.item_type_serializers import ItemTypeSerializerForUser
from features.item.serializers.unit_of_measurement_serializers import UnitOfMeasurementSerializerForUser



class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = ['id', 'name', 'description', 'type',
                  'is_active', 'created_at', 'updated_at']

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


class MedicineDosageUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicineDosageUnit
        fields = ['id', 'name', 'description','example','dosage_example', 'is_active']

class ItemDetailSerializerForReport(serializers.ModelSerializer):
    type = ItemTypeSerializerForUser(read_only=True)
    item_batches = ItemBatchSerializer(many=True, read_only=True)
    unit_of_measurement = UnitOfMeasurementSerializerForUser(read_only=True)
    quantity_in_stock = serializers.IntegerField(read_only=True)
    packaging=ItemPackagingSerializer(read_only=True)
    medicine_dosage_unit = MedicineDosageUnitSerializer(many=True, read_only=True)

    # ---- get all the 


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        item_stock_info = ItemStockInfo.get_latest_by_item_id(instance.id)
        quantity_in_stock = item_stock_info.item_quantity_in_stock if item_stock_info else 0
        representation['quantity_in_stock'] = quantity_in_stock
   
    
        return representation

    class Meta:
        model = Item
        fields = ['id', 'name', 'contents','description', 'type', 'unit_of_measurement','item_batches','quantity_in_stock']