from django.forms import model_to_dict
from rest_framework import serializers
from features.supplier.models import Supplier

from features.supplier.serializers import SupplierSerializer
from .models import  InventoryTransaction, InventoryTransactionItem, IndentInventoryTransaction

class InventoryTransactionSerializer(serializers.ModelSerializer):
    inventory_transaction_type = serializers.ChoiceField(choices=InventoryTransaction.TransactionTypes.choices)
    inventory_transaction_id = serializers.CharField(read_only=True)
    
    class Meta:
        model = InventoryTransaction
        fields = [
            'id', 
            'inventory_transaction_type',
            'inventory_transaction_id',
            'date_time',
            'remarks',
            'created_on',
            'updated_on',
            ]

class InventoryTransactionItemSerializer(serializers.ModelSerializer):
    inventory_transaction = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = InventoryTransactionItem
        fields = [
            'id', 
            'inventory_transaction',
            'item_batch',
            'quantity',
            'is_active', 
          
            ]

    # def to_representation(self, instance):
    #     rep = super().to_representation(instance)
    #     rep['date_time'] = instance.inventory_transaction.date_time.strftime('%d-%m-%Y %H:%M')
    #     return rep

class IndentInventoryTransactionSerializer(InventoryTransactionSerializer):
    inventory_transaction_item_set = serializers.ListSerializer(child=InventoryTransactionItemSerializer(), read_only=False)
    # supplier = serializers.PrimaryKeyRelatedField(queryset=Supplier.objects.all())

    # supplier = SupplierSerializer(read_only=True)
    date_time = serializers.SerializerMethodField()
    def get_supplier(self, obj):
        return model_to_dict(obj.supplier)

    class Meta:
        model = IndentInventoryTransaction
        fields = '__all__'
    

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['supplier'] = SupplierSerializer(instance.supplier).data
        return representation

    def create(self, validated_data):
      
        transaction_items_data = validated_data.pop('inventory_transaction_item_set')
       
        transaction = IndentInventoryTransaction.objects.create(**validated_data)
        
        for transaction_item_data in transaction_items_data:
            InventoryTransactionItem.objects.create(inventory_transaction=transaction, **transaction_item_data)
        return transaction
    
    def get_date_time(self, obj):
        return obj.date_time.strftime('%d-%m-%Y %H:%M')