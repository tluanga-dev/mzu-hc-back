from datetime import datetime
from django.forms import model_to_dict
from rest_framework import serializers
from features.helper.format_date_time import format_datetime_with_timezone_offset
from features.supplier.models import Supplier

from features.supplier.serializers import SupplierSerializer
from .models import InventoryTransaction, InventoryTransactionItem, IndentInventoryTransaction

class InventoryTransactionItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = InventoryTransactionItem
        fields = ['id', 'inventory_transaction', 'item_batch', 'quantity', 'is_active']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data.pop('inventory_transaction', None)
        return data

class InventoryTransactionBaseSerializer(serializers.ModelSerializer):
    inventorytransactionitem_set = InventoryTransactionItemSerializer(many=True)

    class Meta:
        model = InventoryTransaction
        fields = ['__all__', 'inventorytransactionitem_set']

    def validate(self, data):
        if 'inventorytransactionitem_set' not in data or not data['inventorytransactionitem_set']:
            raise serializers.ValidationError({"inventorytransactionitem_set": "This field is required."})
        return data

    def create(self, validated_data):
        transaction_items_data = validated_data.pop('inventorytransactionitem_set')
        transaction = super().create(validated_data)
        for transaction_item_data in transaction_items_data:
            InventoryTransactionItem.objects.create(inventory_transaction=transaction, **transaction_item_data)
        return transaction

class IndentInventoryTransactionSerializer(InventoryTransactionBaseSerializer):
    
    supplier = serializers.SerializerMethodField()
    supplyOrderNo = serializers.CharField()
    supplyOrderDate = serializers.DateField()
    dateOfDeliverty = serializers.DateField()
    # inventorytransactionitem_set=serializers.SerializerMethodField()
    inventory_transaction_item = serializers.SerializerMethodField(source='inventorytransactionitem_set')

    # def get_supplier(self, obj):
    #     supplier = obj.supplier
    #     return {
    #         'id': supplier.id,
    #         'name': supplier.name,
    #         # add other fields you want to include
    #     }
    
    def get_supplier(self, obj):
        return model_to_dict(obj.supplier)
    
    # def get_inventory_transaction_items(self, obj):
    #     return model_to_dict(obj.inventorytransactionitem_set.all())
    
    def get_inventory_transaction_item(self, obj):
        return [model_to_dict(item) for item in obj.inventorytransactionitem_set.all()]
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['date_time'] = instance.date_time.strftime('%d-%m-%Y %H:%M')
        return data

    
    class Meta(InventoryTransactionBaseSerializer.Meta):
        model = IndentInventoryTransaction
        # fields = InventoryTransactionBaseSerializer.Meta.fields + ['supplier', 'supplyOrderNo', 'supplyOrderDate', 'dateOfDeliverty']
        # fields = ['supplier', 'supplyOrderNo', 'supplyOrderDate', 'dateOfDeliverty']
        fields = '__all__'