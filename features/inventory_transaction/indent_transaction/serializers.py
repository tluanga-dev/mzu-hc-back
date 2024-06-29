from django.forms import model_to_dict
from features.inventory_transaction.indent_transaction.models import IndentInventoryTransaction
from features.inventory_transaction.inventory_transaction.models import InventoryTransactionItem
from features.inventory_transaction.inventory_transaction.serializers import InventoryTransactionSerializer
from features.supplier.models import Supplier
from features.supplier.serializers import SupplierSerializer
from rest_framework import serializers
import logging

class IndentInventoryTransactionListSerializer(serializers.ModelSerializer):
    supply_order_date = serializers.DateField(format="%d-%m-%Y")
    date_of_delivery = serializers.DateField(format="%d-%m-%Y")

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['supplier'] = SupplierSerializer(instance.supplier).data["name"]

        return representation
    
    class Meta:
        model = IndentInventoryTransaction
        fields = ['id','inventory_transaction_id','supplier', 'supply_order_no', 'supply_order_date', 'date_of_delivery', 'remarks']



class IndentInventoryTransactionDetailSerializer(InventoryTransactionSerializer):
    supply_order_date = serializers.DateField(format="%d-%m-%Y")
    date_of_delivery = serializers.DateField(format="%d-%m-%Y")
    

    def to_representation(self, instance):
        print('inside IndentInventoryTransactionDetailSerializer')
        representation = super().to_representation(instance)
        representation['supplier'] = SupplierSerializer(instance.supplier).data
        
        
        return representation
   
    
    class Meta:
        model = IndentInventoryTransaction
        fields = '__all__'  # Or list all fields explicitly if needed



class IndentInventoryTransactionSerializer(InventoryTransactionSerializer):
    supply_order_date = serializers.DateField(format="%d-%m-%Y")
    date_of_delivery = serializers.DateField(format="%d-%m-%Y")

    def get_supplier(self, obj):
        return model_to_dict(obj.supplier)

    def to_internal_value(self, data):
        if 'supply_order_no' in data:
            print('the inputted supply order ', data['supply_order_no'])
   
        return super().to_internal_value(data)

    class Meta:
        model = IndentInventoryTransaction
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['supplier'] = SupplierSerializer(instance.supplier).data

        return representation