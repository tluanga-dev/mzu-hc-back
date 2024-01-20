from rest_framework import serializers
from .models import ItemStockInfo

class ItemStockInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemStockInfo
        fields = ['id', 'quantity', 'item', 'updated_on']