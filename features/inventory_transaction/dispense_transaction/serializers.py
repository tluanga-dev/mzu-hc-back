from features.inventory_transaction.dispense_transaction import generate_dispense_list
from features.inventory_transaction.dispense_transaction.models import DispenseInventoryTransaction
from features.inventory_transaction.inventory_transaction.models import InventoryTransaction, InventoryTransactionItem
from features.inventory_transaction.inventory_transaction.serializers import InventoryTransactionItemSerializer, InventoryTransactionSerializer
from features.item.models import Item, ItemCategory, ItemType, UnitOfMeasurement

from features.prescription.serializers import PrescriptionSerializer

from rest_framework import serializers

class DispenseItemSerializer(serializers.ModelSerializer):
    item_id = serializers.IntegerField()
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
        fields = ['item', 'quantity']


class DispenseInventoryTransactionSerializer(InventoryTransactionSerializer):
    dispense_item_set = DispenseItemSerializer(many=True, write_only=True)
    inventory_transaction_item_set = InventoryTransactionItemSerializer(many=True, read_only=True)
    def create(self, validated_data):
        try:
            transaction_items_data = validated_data.pop('inventory_transaction_item_set')
            transaction = InventoryTransaction.model.objects.create(**validated_data)
            transaction.save()  # Ensure the transaction is saved
            for transaction_item_data in transaction_items_data:
                data=generate_dispense_list(transaction_item_data.item, transaction_item_data.quantity)
                InventoryTransactionItem.objects.create(inventory_transaction=transaction, **data)
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


