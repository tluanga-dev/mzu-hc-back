from django.forms import model_to_dict
from features.inventory_transaction.indent_transaction.models import IndentInventoryTransaction
from features.inventory_transaction.inventory_transaction.serializers import InventoryTransactionSerializer
from features.supplier.serializers import SupplierSerializer


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