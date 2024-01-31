from rest_framework import serializers
from features.supplier.models import Supplier

from features.supplier.serializers import SupplierSerializer
from .models import  InventoryTransactionItem, IndentInventoryTransaction



class InventoryTransactionItemSerializer(serializers.ModelSerializer):
    inventory_transaction = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = InventoryTransactionItem
        fields = ['id', 'inventory_transaction', 'item_batch', 'quantity', 'is_active', 'created_on', 'updated_on']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['date_time'] = instance.inventory_transaction.date_time.strftime('%d-%m-%Y %H:%M')
        return rep

class IndentInventoryTransactionSerializer(serializers.ModelSerializer):
    inventory_transaction_item = serializers.ListSerializer(child=InventoryTransactionItemSerializer(), write_only=True)
    supplier = serializers.PrimaryKeyRelatedField(queryset=Supplier.objects.all())


    class Meta:
        model = IndentInventoryTransaction
        fields = ['id', 'inventory_transaction_type', 'inventory_transaction_id', 'status', 'supplier', 'supplyOrderNo', 'supplyOrderDate', 'dateOfDeliverty', 'remarks', 'date_time', 'inventory_transaction_item']

    def get_inventory_transaction_item(self, obj):
        return InventoryTransactionItemSerializer(obj.inventorytransactionitem_set.all(), many=True).data

    
    def create(self, validated_data):
        # print('------Validated Data------')
        # print(validated_data)
        transaction_items_data = validated_data.pop('inventory_transaction_item', [])
        # print('------Transaction Items Data------')
        # print(transaction_items_data)
        transaction = super().create(validated_data)
        for transaction_item_data in transaction_items_data:
           result= InventoryTransactionItem.objects.create(inventory_transaction=transaction, **transaction_item_data)
        #    print('------Result------')
        #    print(result)
        return transaction