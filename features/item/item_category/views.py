from rest_framework import viewsets
from .models import ItemCategory
from .serializers import ItemCategorySerializer

class ItemCategoryViewSet(viewsets.ModelViewSet):
    queryset = ItemCategory.objects.all()
    serializer_class = ItemCategorySerializer