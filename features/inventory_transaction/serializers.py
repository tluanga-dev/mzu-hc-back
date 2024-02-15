from django.forms import model_to_dict
from rest_framework import serializers
from features.item.models import Item


from features.organisation_section.serializers import OrganisationSectionSerializer
from features.supplier.models import Supplier

from features.supplier.serializers import SupplierSerializer
from .models import  InventoryTransaction, InventoryTransactionItem, IndentInventoryTransaction, IssueItemInventoryTransaction, ItemStockInfo


class InventoryTransactionItemSerializer(serializers.ModelSerializer):
    inventory_transaction = serializers.PrimaryKeyRelatedField(read_only=True)
    inventory_transaction_type = serializers.SerializerMethodField()  

    def get_inventory_transaction_type(self, obj):
        return obj.inventory_transaction.inventory_transaction_type
    
    class Meta:
        model = InventoryTransactionItem
        fields = [
            'id', 
            'inventory_transaction',
            'item_batch',
            'quantity',
            'is_active', 
            'inventory_transaction_type'
          
            ]


class InventoryTransactionSerializer(serializers.ModelSerializer):
   
    inventory_transaction_id = serializers.CharField(read_only=True)
    inventory_transaction_item_set = serializers.ListSerializer(
        child=InventoryTransactionItemSerializer(),
        read_only=False
    )
    inventory_transaction_type=serializers.CharField(read_only=True)
    date_time = serializers.SerializerMethodField()

    def create(self, validated_data):
        try:
            # print(f"validated_data: {validated_data}")
            transaction_items_data = validated_data.pop('inventory_transaction_item_set')
            transaction = self.Meta.model.objects.create(**validated_data)
            
            for transaction_item_data in transaction_items_data:
                data=InventoryTransactionItem.objects.create(inventory_transaction=transaction, **transaction_item_data)
                
            return transaction
      
        except ValueError as e:
            print(f"ValueError: {e}")
            raise serializers.ValidationError(str(e))
        
    def update(self, instance, validated_data):
        # Handle nested updates manually
        transaction_items_data = validated_data.pop('inventory_transaction_item_set')
        for item_data in transaction_items_data:
            item_id = item_data.get('id', None)
            if item_id:
                # Update existing items
                item = instance.inventory_transaction_item_set.get(id=item_id)
                for attr, value in item_data.items():
                    setattr(item, attr, value)
                item.save()
            else:
                # Create new items
                InventoryTransactionItem.objects.create(inventory_transaction=instance, **item_data)

        # Update other fields normally
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance
    
    def get_date_time(self, obj):
        return obj.date_time.strftime('%d-%m-%Y %H:%M')
    

    class Meta:
        model = InventoryTransaction
        fields = [
            'id', 
            'inventory_transaction_type',
            'inventory_transaction_id',
            'inventory_transaction_item_set'
            'date_time',
            'remarks',
            'created_on',
            'updated_on',
            ]
        read_only_fields = [
            'id','inventory_transaction_type',
            'inventory_transaction_id',
            'created_on',
            'updated_on'
        ]



class IndentInventoryTransactionSerializer(InventoryTransactionSerializer):
    def get_supplier(self, obj):
        return model_to_dict(obj.supplier)
    
    class Meta:
        model = IndentInventoryTransaction
        fields = '__all__'
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['supplier'] = SupplierSerializer(instance.supplier).data
        return representation

class ItemStockInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model=ItemStockInfo
        fields='__all__'  
    

class IssueItemInventoryTransactionSerializer(InventoryTransactionSerializer):
   
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['issue_to'] = OrganisationSectionSerializer(instance.issue_to).data
        return representation
    
    class Meta:
        model = IssueItemInventoryTransaction
        fields = '__all__'

class ItemTransactionDetailSerializer(serializers.ModelSerializer):
    item_stock_info = serializers.SerializerMethodField()
    transactions = serializers.SerializerMethodField()

    # def to_representation(self, instance):
    #      # Print the related ItemStockInfo instance
    
    #     item_stock=ItemStockInfo.objects.first()
   
      
    #     representation = super().to_representation(instance)
    #     return representation

    def get_item_stock_info(self, obj):
        item_stock=ItemStockInfo.objects.filter(item=obj).last()
       
        return ItemStockInfoSerializer(item_stock).data
    
    def get_transactions(self, obj):
        inventory_transaction_items = InventoryTransactionItem.objects.filter(item_batch__in=obj.item_batches.all())

        return InventoryTransactionItemSerializer(inventory_transaction_items, many=True).data


    class Meta:
        model = Item
        fields = ['id', 'name','item_code',  'transactions', 'item_stock_info']