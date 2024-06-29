from rest_framework.response import Response
from rest_framework import viewsets,status
from django_filters import rest_framework as filters
from features.core.utils.convert_date import DateConverter
from features.inventory_transaction.indent_transaction.models import IndentInventoryTransaction
from features.inventory_transaction.indent_transaction.serializers import  IndentInventoryTransactionDetailSerializer, IndentInventoryTransactionListSerializer, IndentInventoryTransactionSerializer
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend

from features.item.serializers.item_with_batch_stock_info_serializer import ItemDetailWithBatchStockInfoSerializer

class StandardResultsSetPagination(PageNumberPagination):
    """Standard pagination settings for the API results."""
    page_size = 8
    page_size_query_param = 'page_size'
    max_page_size = 100

class IndentInventoryTransactionFilter(filters.FilterSet):
    supplier = filters.CharFilter(field_name='supplier', lookup_expr='icontains')
    supply_order_no = filters.CharFilter(field_name='supply_order_no', lookup_expr='icontains')
    supply_order_date = filters.CharFilter(method='filter_supply_order_date')
    supply_order_date_range = filters.CharFilter(method='filter_supply_order_date_range')

    class Meta:
        model = IndentInventoryTransaction
        fields = ['supplier', 'supply_order_no', 'supply_order_date', 'supply_order_date_range']

    def filter_supply_order_date(self, queryset, name, value):
        return queryset.filter(supply_order_date__exact=DateConverter.convert_date_time_format_to_django_default(value))

    def filter_supply_order_date_range(self, queryset, name, value):
        date_from, date_to = value.split(',')
        return queryset.filter(
            supply_order_date__gte=DateConverter.convert_date_time_format_to_django_default(date_from),
            supply_order_date__lte=DateConverter.convert_date_time_format_to_django_default(date_to)
        )

class IndentInventoryTransactionViewSet(viewsets.ModelViewSet):
    queryset = IndentInventoryTransaction.objects.all()
    serializer_class = IndentInventoryTransactionListSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = IndentInventoryTransactionFilter
    def get_paginate_queryset(self, queryset):
        page_size = self.request.query_params.get('page_size', None)
        if page_size:
            try:
                page_size = int(page_size)
                self.pagination_class.page_size = min(page_size, self.pagination_class.max_page_size)
            except ValueError:
                pass
        return super().paginate_queryset(queryset)
    
    def get_serializer_class(self):
        detail_flag = self.request.query_params.get('detail', '1')
        if detail_flag == '1':
            return IndentInventoryTransactionListSerializer
        elif detail_flag == '2':
            return IndentInventoryTransactionDetailSerializer
        return IndentInventoryTransactionDetailSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = IndentInventoryTransactionDetailSerializer(instance)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        print('Inside IndentInventoryTransactionViewSet create method')
        print('Request data:', request.data)
        serializer = IndentInventoryTransactionSerializer(data=request.data)
        if(serializer.is_valid()):
            print('serializer.validated_data',serializer.validated_data)
        else:
            print('serializer.errors',serializer.errors)
        serializer.is_valid(raise_exception=True)
        print('serializer.validated_data',serializer.validated_data)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def perform_create(self, serializer):
        print('Inside perform_create method of IndentInventoryTransactionViewSet')
        serializer.save()

