
from rest_framework import serializers
from features.item.models import Item, ItemBatch


from features.organisation_section.serializers import OrganisationSectionSerializer
from features.utils.convert_date import DateConverter



from .models import  InventoryTransaction, InventoryTransactionItem, ItemStockInfo


class InventoryTransactionItemSerializer(serializers.ModelSerializer):
    inventory_transaction = serializers.PrimaryKeyRelatedField(read_only=True)
    # inventory_transaction_type = serializers.SerializerMethodField() 
    item=serializers.SerializerMethodField()

    def get_item(self,obj):
        item={
            'name': obj.item_batch.item.name,
            'type':obj.item_batch.item.type.name
        }
        return  item

    # def get_inventory_transaction_type(self, obj):
    #     return obj.inventory_transaction.inventory_transaction_type
    
    class Meta:
        model = InventoryTransactionItem
        fields = [
            'id', 
            'item',
            'inventory_transaction',
            'item_batch',
            'quantity',
            # 'inventory_transaction_type'
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
        fields=['id','inventory_transaction_item','quantity']  
    

class ItemTransactionDetailSerializerV1(serializers.ModelSerializer):
    item_stock_info = serializers.SerializerMethodField()
    transactions = serializers.SerializerMethodField()
    type=serializers.SerializerMethodField()
    unit_of_measurement=serializers.SerializerMethodField()

    def get_type(self, obj):
        return obj.type.name
    
    def get_unit_of_measurement(self, obj):
        return obj.unit_of_measurement.abbreviation

    def get_item_stock_info(self, obj):
        item_stock=ItemStockInfo.get_latest_by_item_id(obj.id)
       
        return item_stock.quantity
    
    def get_transactions(self, obj):
        inventory_transaction_items = InventoryTransactionItem.objects.filter(item_batch__in=obj.item_batches.all())

        return InventoryTransactionItemSerializer(inventory_transaction_items, many=True).data


    class Meta:
        model = Item
        fields = ['id', 'name','item_code', 'type','unit_of_measurement', 'transactions', 'item_stock_info']


class ItemBatchStockInfoSerializer(serializers.ModelSerializer):
    quantity_in_stock = serializers.SerializerMethodField()
    def get_quantity_in_stock(self, obj):
        
        return obj.quantity_in_stock
    class Meta:
        model = ItemBatch
        fields=['batch_id']

class ItemTransactionDetailSerializer(serializers.ModelSerializer):
    quantity_in_stock = serializers.SerializerMethodField()
    transactions = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()
    unit_of_measurement = serializers.SerializerMethodField()
  


    def get_item_batch_stock_info(self, obj):
        return ItemBatchStockInfoSerializer(obj.item_batches.all(), many=True).data


    
    def get_type(self, obj):
        return obj.type.name if obj.type else None
    
    def get_unit_of_measurement(self, obj):
        return obj.unit_of_measurement.abbreviation if obj.unit_of_measurement else None

    def get_quantity_in_stock(self, obj):
        # Debugging: Fetch all stock info entries related to the item
        # stock_infos = ItemStockInfo.objects.filter(item=obj)
        # print("All Stock Infos:", stock_infos)  # This will print the query set of all related stock info objects
        
        # # Get the last entry
        # last_stock_info = stock_infos.last()
        # print("Last Stock Info:", last_stock_info)  # This will show the last stock info object if any
        
        last_stock_info = ItemStockInfo.get_latest_by_item_id(obj.id)
        if last_stock_info:
            return last_stock_info.quantity
        return 0
        
    def get_transactions(self, obj):
        inventory_transaction_items = InventoryTransactionItem.objects.filter(item_batch__in=obj.item_batches.all())
        return InventoryTransactionItemSerializer(inventory_transaction_items, many=True).data

    class Meta:
        model = Item
        fields = [
            'id',
            'name', 
            'item_code', 
            'type', 
            'unit_of_measurement', 
            'transactions', 
            'quantity_in_stock',
         
        ]