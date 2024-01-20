from rest_framework import viewsets

from features.item.item.models import Item
from features.item.item.serializers import ItemSerializer
class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer