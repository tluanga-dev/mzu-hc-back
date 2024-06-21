# myapp/views.py

from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
import django_filters.rest_framework
from .models import Item, MedicineDosage
from .serializers import MedicineSerializer, MedicineDosageSerializer, MedicineWithStockInfoSerializer

class StandardResultsSetPagination(PageNumberPagination):
    """Standard pagination settings for the API results."""
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class MedicineDosageViewSet(viewsets.ModelViewSet):
    queryset = MedicineDosage.objects.all()
    serializer_class = MedicineDosageSerializer

class MedicineFilter(django_filters.FilterSet):
    item_id = django_filters.CharFilter(field_name='id', lookup_expr='icontains')
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    type = django_filters.CharFilter(field_name='type__name', lookup_expr='icontains')

    class Meta:
        model = Item
        fields = ['item_id', 'name', 'type']

class MedicineViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.filter(type__category__name='Medicine')
    serializer_class = MedicineWithStockInfoSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_class = MedicineFilter
    pagination_class = StandardResultsSetPagination

    # def get_queryset(self):
    #     qs = super().get_queryset()
    #     print(f"Queryset count: {qs.count()}")
    #     return qs