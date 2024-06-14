# features/common/views.py

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from features.item.serializers.item_with_batch_stock_info_serializer import ItemWithBatchStockInfoSerializer
from features.item.models import Item
from django_filters import rest_framework as filters


class StandardResultsSetPagination(PageNumberPagination):
    """Standard pagination settings for the API results."""
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class ItemWithBatchStockInfoFilter(filters.FilterSet):
    item_id = filters.CharFilter(field_name='id', lookup_expr='icontains')
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    type = filters.CharFilter(field_name='type__name', lookup_expr='icontains')
   
    class Meta:
        model = Item
        fields = ['item_id', 'name', 'type']


class ItemWithBatchStockInfoViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A viewset for listing and retrieving items with batch stock info.
    """
    queryset = Item.objects.all()
    serializer_class = ItemWithBatchStockInfoSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = ItemWithBatchStockInfoFilter
