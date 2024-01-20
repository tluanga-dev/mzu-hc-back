
from rest_framework import serializers
from features.item.item.models import Item

from features.item.item_type.serializers import ItemTypeSerializer
from features.transaction.item_stock_info.serializers import ItemStockInfoSerializer

class ItemSerializer(serializers.ModelSerializer):
    type = ItemTypeSerializer()
    item_stock_info = ItemStockInfoSerializer()

    class Meta:
        model = Item
        fields = '__all__'