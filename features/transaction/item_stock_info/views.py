from rest_framework import viewsets
from .models import ItemStockInfo
from .serializers import ItemStockInfoSerializer

class ItemStockInfoViewSet(viewsets.ModelViewSet):
    queryset = ItemStockInfo.objects.all()
    serializer_class = ItemStockInfoSerializer