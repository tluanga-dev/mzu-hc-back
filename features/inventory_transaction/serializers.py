from rest_framework import serializers
from features.supplier.models import Supplier

from features.supplier.serializers import SupplierSerializer
from .models import InventoryTransaction, InventoryTransactionItem, IndentInventoryTransaction

class InventoryTransactionItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryTransactionItem
        fields = '__all__'

class InventoryTransactionBaseSerializer(serializers.ModelSerializer):
    inventorytransactionitem_set = InventoryTransactionItemSerializer(many=True)

    class Meta:
        model = InventoryTransaction
        fields =  ['__all__' ,'inventorytransactionitem_set']

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

    def get_supplier(self, obj):
        supplier = obj.supplier
        return {
            'id': supplier.id,
            'name': supplier.name,
            # add other fields you want to include
        }


    class Meta(InventoryTransactionBaseSerializer.Meta):
        model = IndentInventoryTransaction
        # fields = InventoryTransactionBaseSerializer.Meta.fields + ['supplier', 'supplyOrderNo', 'supplyOrderDate', 'dateOfDeliverty']
        # fields = ['supplier', 'supplyOrderNo', 'supplyOrderDate', 'dateOfDeliverty']
        fields = '__all__'