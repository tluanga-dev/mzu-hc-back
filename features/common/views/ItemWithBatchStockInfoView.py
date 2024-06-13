# features/common/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from features.common.serializers.item_with_batch_stock_info_serializer import ItemWithBatchStockInfoSerializer
from features.item.models import Item

class ItemWithBatchStockInfoListView(APIView):
    """
    A view for listing all items with batch stock info.
    """
    def get(self, request, format=None):
        items = Item.objects.all()
        serializer = ItemWithBatchStockInfoSerializer(items, many=True)
        return Response(serializer.data)
