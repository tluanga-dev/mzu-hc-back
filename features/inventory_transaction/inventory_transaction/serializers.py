
from rest_framework import serializers
from features.item.models import Item


from features.organisation_section.serializers import OrganisationSectionSerializer
from features.utils.convert_date import DateConverter



from .models import  InventoryTransaction, InventoryTransactionItem, ItemStockInfo


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
    created_on = serializers.DateTimeField(format="%d-%m-%Y %H:%M:%S")
    updated_on = serializers.DateTimeField(format="%d-%m-%Y %H:%M:%S", read_only=True)

    inventory_transaction_id = serializers.CharField(read_only=True)
    inventory_transaction_item_set = serializers.ListSerializer(
        child=InventoryTransactionItemSerializer(),
        read_only=False
    )
    inventory_transaction_type=serializers.CharField(read_only=True)
    created_on = serializers.SerializerMethodField()

    def create(self, validated_data):
        try:
            transaction_items_data = validated_data.pop('inventory_transaction_item_set')
            transaction = self.Meta.model.objects.create(**validated_data)
            transaction.save()  # Ensure the transaction is saved
            for transaction_item_data in transaction_items_data:
                InventoryTransactionItem.objects.create(inventory_transaction=transaction, **transaction_item_data)
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
    
    def get_created_on(self, obj):
        return obj.created_on.strftime('%d-%m-%Y %H:%M')
    

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
            
        ]


class ItemStockInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model=ItemStockInfo
        fields='__all__'  
    

class ItemTransactionDetailSerializer(serializers.ModelSerializer):
    item_stock_info = serializers.SerializerMethodField()
    transactions = serializers.SerializerMethodField()

    def get_item_stock_info(self, obj):
        item_stock=ItemStockInfo.objects.filter(item=obj).last()
       
        return ItemStockInfoSerializer(item_stock).data
    
    def get_transactions(self, obj):
        inventory_transaction_items = InventoryTransactionItem.objects.filter(item_batch__in=obj.item_batches.all())

        return InventoryTransactionItemSerializer(inventory_transaction_items, many=True).data


    class Meta:
        model = Item
        fields = ['id', 'name','item_code',  'transactions', 'item_stock_info']