from features.inventory_transaction.dispense_transaction.models import DispenseInventoryTransaction
from features.inventory_transaction.inventory_transaction.serializers import InventoryTransactionSerializer
from features.item.models import Item, ItemCategory, ItemType, UnitOfMeasurement
from features.prescription.models import Prescription
from features.prescription.serializers import PrescriptionSerializer

from rest_framework import serializers


class DispenseInventoryTransactionSerializer(InventoryTransactionSerializer):
   
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['prescription'] = PrescriptionSerializer(instance.prescription).data
        return representation
    
    class Meta:
        model = DispenseInventoryTransaction
        fields = '__all__'



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

class ItemInformationForDispenseTransactionSerializer(serializers.ModelSerializer):
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['type'] = ItemTypeSerializerForDispense(instance.type).data
        representation['unit_of_measurement']=UnitOfMeasurementSerializerForDispense(instance.unit_of_measurement).data

        return representation
    
    class Meta:
        model = Item
        fields = ['id', 'name']


