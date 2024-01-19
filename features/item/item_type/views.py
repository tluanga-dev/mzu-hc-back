# views.py

from rest_framework import viewsets
from .models import ItemType
from .serializers import ItemTypeSerializer

class ItemTypeViewSet(viewsets.ModelViewSet):
    queryset = ItemType.objects.all()
    serializer_class = ItemTypeSerializer