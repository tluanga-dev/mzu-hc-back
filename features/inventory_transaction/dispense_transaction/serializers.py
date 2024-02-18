from features.inventory_transaction.indent_transaction.serializers import IndentInventoryTransactionSerializer
from features.inventory_transaction.inventory_transaction.serializers import InventoryTransactionSerializer
from features.prescription.serializers import PrescriptionSerializer


class DispenseInventoryTransactionSerializer(InventoryTransactionSerializer):
   
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['prescription'] = PrescriptionSerializer(instance.prescription).data
        return representation
    
    class Meta:
        model = IndentInventoryTransactionSerializer
        fields = '__all__'