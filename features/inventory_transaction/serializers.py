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
    inventorytransactionitem_set = serializers.ListSerializer(child=InventoryTransactionItemSerializer(), read_only=False)
    supplier = serializers.PrimaryKeyRelatedField(queryset=Supplier.objects.all())

    class Meta:
        model = IndentInventoryTransaction
        fields = '__all__'
        
    def create(self, validated_data):
        print('validated_data',validated_data)
        transaction_items_data = validated_data.pop('inventorytransactionitem_set')
        transaction = IndentInventoryTransaction.objects.create(**validated_data)
        for transaction_item_data in transaction_items_data:
            InventoryTransactionItem.objects.create(inventory_transaction=transaction, **transaction_item_data)
        return transaction