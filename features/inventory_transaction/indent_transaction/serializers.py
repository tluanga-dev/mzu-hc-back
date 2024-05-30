from django.forms import model_to_dict
from features.inventory_transaction.indent_transaction.models import IndentInventoryTransaction
from features.inventory_transaction.inventory_transaction.serializers import InventoryTransactionSerializer
from features.item.serializers import ItemBatchSerializer
from features.supplier.serializers import SupplierSerializer
from features.utils.convert_date import DateConverter
from rest_framework import serializers


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
        representation = super().to_representation(instance)
        representation['supplier'] = SupplierSerializer(instance.supplier).data
        
        
        return representation
    
    class Meta:
        model = IndentInventoryTransaction
        fields = '__all__'  # Or list all fields explicitly if needed

# class IndentInventoryTransactionSerializer(InventoryTransactionSerializer):
#     supply_order_date = serializers.DateField(format="%d-%m-%Y")
#     date_of_delivery = serializers.DateField(format="%d-%m-%Y")

#     def get_supplier(self, obj):
#         return model_to_dict(obj.supplier)

#     def to_internal_value(self, data):
#         # if 'supply_order_no' in data:
#         #     print('the inputted supply order ', data['supply_order_no'])

#     # def to_internal_value(self, data):
#     #     # Convert the incoming date_and_time to the database format

#     #     if 'supply_order_date' in data:
#     #         try:
#     #             print('before conversion',data['supply_order_date'])
#     #             converted_date_and_time= DateConverter.convert_date_format(
#     #                 data['supply_order_date']
#     #             )

#     #             data['supply_order_date'] =converted_date_and_time
#     #             print('after converison',data['supply_order_date'])
#     #         except ValueError:
#     #             raise serializers.ValidationError({"supply_order_date": "Date of expiry must be in 'dd-mm-yyyy hh:mm' format"})

#     #     if 'date_of_delivery' in data:
#     #         try:
#     #             print('before conversion',data['date_of_delivery'])
#     #             converted_date_and_time= DateConverter.convert_date_format(
#     #                 data['date_of_delivery']
#     #             )

#     #             data['date_of_delivery'] =converted_date_and_time
#     #             print('after date_of_delivery',data['date_of_delivery'])
#     #         except ValueError:
#     #             raise serializers.ValidationError({"date_of_delivery": "Date of expiry must be in 'dd-mm-yyyy hh:mm' format"})

#         return super().to_internal_value(data)

#     class Meta:
#         model = IndentInventoryTransaction
#         fields = '__all__'

#     def to_representation(self, instance):
#         representation = super().to_representation(instance)
#         representation['supplier'] = SupplierSerializer(instance.supplier).data

#         return representation
