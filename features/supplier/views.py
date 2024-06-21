from rest_framework import viewsets

from features.item.views import StandardResultsSetPagination
from .models import Supplier
from .serializers import SupplierSerializer

class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    pagination_class = StandardResultsSetPagination