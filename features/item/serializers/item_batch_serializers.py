from rest_framework import serializers

from features.core.serializers.custom_date_field_serializer import CustomDateField
from features.inventory_transaction.inventory_transaction.models import ItemStockInfo
from features.item.models import Item, ItemBatch

class ItemBatchSerializer(serializers.ModelSerializer):
    date_of_expiry = CustomDateField()

   
    class Meta:
        model = ItemBatch
        fields = ['id', 'batch_id', 'description', 'date_of_expiry',
                  'item', 'is_active', 'created_at', 'updated_at']
        
class ItemBatchWithStockInfoSerializer(serializers.ModelSerializer):
    date_of_expiry = CustomDateField()
    quantity_in_stock = serializers.SerializerMethodField()
    def get_quantity_in_stock(self, obj):
        item_stock_info = ItemStockInfo.get_latest_stock_info_of_item_batch(obj.id)
        return 0 if item_stock_info is None else item_stock_info.item_quantity_in_stock
    class Meta:
        model = ItemBatch
        fields = ['id', 'batch_id', 'description', 'date_of_expiry','quantity_in_stock',
                  'item', 'is_active', 'created_at', 'updated_at']
        
        