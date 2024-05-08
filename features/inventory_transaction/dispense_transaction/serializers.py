from features.inventory_transaction.dispense_transaction.generate_dispense_list import generate_dispense_list
from features.inventory_transaction.dispense_transaction.models import DispenseInventoryTransaction
from features.inventory_transaction.inventory_transaction.models import InventoryTransaction, InventoryTransactionItem
from features.inventory_transaction.inventory_transaction.serializers import InventoryTransactionItemSerializer, InventoryTransactionSerializer
from features.item.models import Item, ItemCategory, ItemType, UnitOfMeasurement

from features.prescription.serializers import PrescriptionSerializer

from rest_framework import serializers

from features.utils.print_json import print_json_string

class DispenseItemSerializer(serializers.ModelSerializer):
    item_id = serializers.UUIDField()
    quantity = serializers.IntegerField()
    def validate(self, data):
        # Optionally, add validation to check if item exists and quantity is sufficient
        item = Item.objects.filter(id=data['item_id']).first()
        if not item:
            raise serializers.ValidationError("Item with given ID does not exist.")
        # You could also check for stock levels here if applicable
        return data
    class Meta:
        model = InventoryTransactionItem
        fields = ['item_id', 'quantity']


class DispenseInventoryTransactionSerializer(InventoryTransactionSerializer):
    dispense_item_set = DispenseItemSerializer(many=True, write_only=True)
    inventory_transaction_item_set = serializers.SerializerMethodField()

    def get_inventory_transaction_item_set(self, instance):
        print('Inside get_inventory_transaction_item_set')
        inventory_transaction_items = instance.inventory_transaction_item_set.all()
        print(inventory_transaction_items)
        serialized_items = []
        item_data={}
        for item in inventory_transaction_items:
            item_data:InventoryTransactionItem=item
            item_batch = item_data.item_batch
           
            item_id = item_batch.item.id
            item_name = item_batch.item.name
            quantity = item.quantity
            # Access other attributes of the item as needed
            print('item id',item_id)
            print('item name',item_name)
            print('item quantity',quantity)

            item_existed_in_serialized_item = None
            for serialized_item in serialized_items:
                if serialized_item['item_id'] == item_id:
                    item_existed_in_serialized_item= serialized_item

            if(item_existed_in_serialized_item):
                item_existed_in_serialized_item['total_quantity_dispense'] += quantity
                item_existed_in_serialized_item['transaction'].append({
                    "id": item.id,
                    "item_batch_id": item_batch.batch_id,
                    "inventory_transaction": item.inventory_transaction.id,
                    "item_batch": item.item_batch.id,
                    "quantity": item.quantity
                })
            else:
                item_data={
                    "item_id": item_id,
                    "item_name": item_name,
                    "total_quantity_dispense":quantity,
                    "transaction": [{
                        "id": item.id,
                        "item_batch_id": item_batch.batch_id,
                        "inventory_transaction": item.inventory_transaction.id,
                        "item_batch": item.item_batch.id,
                        "quantity": item.quantity
                    }]
                }
                serialized_items.append(item_data)
            print('serialized_items')
            for serialized_item in serialized_items:
                
                print(serialized_item)
                print('\n')
            print('search result',item)
           
        
        #     quantity=quantity+item_data["item_quantity"]
        #     item_data={
        #             "item_id": item_id,
        #             "item_name": item_name,
        #             "total_quantity_dispense":quantity,
        #             "transaction": {
        #                 "id": item.id,
        #                 "item_batch_id": item.item_batch,
        #                 "inventory_transaction": item.inventory_transaction.id,
        #                 "item_batch": item.item_batch,
        #                 "quantity": item.quantity
        #             }
        #     }
        
        # serialized_items.append(item_data)
   
        # return inventory_transaction_items
        return serialized_items

    def create(self, validated_data):
        try:
            transaction_items_data = validated_data.pop('dispense_item_set')
            transaction = DispenseInventoryTransaction.objects.create(**validated_data)
            transaction.save()  # Ensure the transaction is saved
            for transaction_item_data in transaction_items_data:
                datas = generate_dispense_list(transaction, transaction_item_data['item_id'], transaction_item_data['quantity'])
                for data in datas:
                    InventoryTransactionItem.objects.create(
                        inventory_transaction=transaction,
                        item_batch=data.item_batch,
                        quantity=data.quantity
                    )
            return transaction
        except ValueError as e:
            print(f"ValueError: {e}")
            raise serializers.ValidationError(str(e))

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['prescription'] = PrescriptionSerializer(instance.prescription).data
        return representation
    
    class Meta:
        model = DispenseInventoryTransaction
        fields ='__all__'



# ----------------------For Fetching item information-------------

class ItemCategorySerializerForDispense(serializers.ModelSerializer):
    class Meta:
        model = ItemCategory
        fields = ['id', 'name', 'abbreviation', 'description']

        
class ItemTypeSerializerForDispense(serializers.ModelSerializer):
    category = ItemCategorySerializerForDispense(read_only=True)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['category'] = ItemCategorySerializerForDispense(
            instance.category).data
        return representation

    class Meta:
        model = ItemType
        fields = ['id', 'name', 'abbreviation',
                  'description', 'example', 'category']
        
class UnitOfMeasurementSerializerForDispense(serializers.ModelSerializer):
  
    class Meta:
        model = UnitOfMeasurement
        fields = ['id', 'name', 'abbreviation', 'description']


