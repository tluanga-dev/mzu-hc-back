from datetime import datetime
from django.forms import model_to_dict
from rest_framework import serializers
from features.helper.format_date_time import format_datetime_with_timezone_offset
from features.supplier.models import Supplier

from features.supplier.serializers import SupplierSerializer
from .models import InventoryTransaction, InventoryTransactionItem, IndentInventoryTransaction

class InventoryTransactionItemSerializer(serializers.ModelSerializer):

    # def to_representation(self, instance):
    #     data = super().to_representation(instance)
    #     # Format datetime fields here
    #     data['created_on'] = instance.created_on
    #     data['updated_on'] = instance.updated_on
       
    #     # Assuming data['created_on'] is a datetime.datetime object
    #     datetime_obj = data['created_on']

    #     # Format datetime object to exclude seconds and microseconds
    #     data['created_on'] = datetime_obj.strftime('%Y-%m-%d %H:%M:%z')

    #     # Assuming data['created_on'] is a datetime.datetime object
    #     datetime_obj =  data['updated_on']

    #     # Format datetime object to exclude seconds and microseconds
    #     data['updated_on']= datetime_obj.strftime('%Y-%m-%d %H:%M:%z')

    #      # Output: Formatted datetime string without seconds and microseconds
    #     return data

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
    inventorytransactionitem_set=serializers.SerializerMethodField()
    

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
    
    def get_inventorytransactionitem_set(self, obj):
        return [model_to_dict(item) for item in obj.inventorytransactionitem_set.all()]


    class Meta(InventoryTransactionBaseSerializer.Meta):
        model = IndentInventoryTransaction
        # fields = InventoryTransactionBaseSerializer.Meta.fields + ['supplier', 'supplyOrderNo', 'supplyOrderDate', 'dateOfDeliverty']
        # fields = ['supplier', 'supplyOrderNo', 'supplyOrderDate', 'dateOfDeliverty']
        fields = '__all__'