from datetime import datetime
from rest_framework import serializers
from features.inventory_transaction.inventory_transaction.models import ItemStockInfo
from features.item.models import Item



class PrescribeMedicineItemSerializer(serializers.ModelSerializer):
    quantity_in_stock=serializers.SerializerMethodField()
    def get_quantity_in_stock(self, obj):
        # quantity_in_stock=ItemStockInfo.get_latest_by_item_id(obj.id).quantity_in_stock
        #  Fetch the latest stock information by item ID
        item_stock_info = ItemStockInfo.get_latest_by_item_id(obj.id)

        # Check if item_stock_info is None and assign 0 if so, otherwise get the quantity_in_stock
        quantity_in_stock = 0 if item_stock_info is None else item_stock_info.item_quantity_in_stock
        return quantity_in_stock

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Accessing only the name of the unit of measurement
        representation['unit_of_measurement'] = instance.unit_of_measurement.abbreviation if instance.unit_of_measurement else None
        return representation

    class Meta:
        model = Item
        fields = ['id', 'name', 'contents', 'unit_of_measurement','quantity_in_stock']