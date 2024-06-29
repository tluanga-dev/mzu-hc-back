# views.py
from django.http import Http404
from rest_framework import status
import django_filters.rest_framework
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from features.item.serializers.item_batch_serializers import ItemBatchSerializer
from features.item.serializers.item_category_serializer import ItemCategorySerializer
from features.item.serializers.item_serializers import ItemDetailSerializerForReport, ItemSerializerForUser, ItemWithStockInfoSerializer
from features.item.serializers.item_type_serializers import ItemTypeSerializer
from features.item.serializers.item_with_batch_stock_info_serializer import ItemDetailWithBatchStockInfoSerializer
from features.item.serializers.unit_of_measurement_serializers import UnitOfMeasurementSerializer
from .models import Item, ItemBatch, ItemCategory, ItemType, UnitOfMeasurement

class StandardResultsSetPagination(PageNumberPagination):
    """Standard pagination settings for the API results."""
    page_size = 8
    page_size_query_param = 'page_size'
    max_page_size = 100


class UnitOfMeasurementViewSet(viewsets.ModelViewSet):
    queryset = UnitOfMeasurement.objects.all()
    serializer_class = UnitOfMeasurementSerializer


class ItemCategoryViewSet(viewsets.ModelViewSet):
    queryset = ItemCategory.objects.all()
    serializer_class = ItemCategorySerializer


class ItemTypeViewSet(viewsets.ModelViewSet):
    queryset = ItemType.objects.all()
    serializer_class = ItemTypeSerializer





# -----Item Stock info viewset--
class ItemWithStockInfoFilter(django_filters.FilterSet):
    item_id = django_filters.CharFilter(field_name='id', lookup_expr='icontains')
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    type = django_filters.CharFilter(field_name='type__name', lookup_expr='icontains')
    category = django_filters.CharFilter(field_name='type__category__name', lookup_expr='icontains')
   
    class Meta:
        model = Item
        fields = ['item_id', 'name','category']

class ItemWithStockInfoViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemWithStockInfoSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_class = ItemWithStockInfoFilter
    pagination_class = StandardResultsSetPagination

class ItemBatchViewSet(viewsets.ModelViewSet):
    queryset = ItemBatch.objects.all()
    serializer_class = ItemBatchSerializer

    @action(detail=True, url_path='item-batches')
    def item_batches_by_item_id(self, request, item_id=None):

        item_batches = self.get_queryset().filter(item=item_id)
        serializer = self.get_serializer(item_batches, many=True)
        return Response(serializer.data)

    def create(self, request, item_id=None):
        try:
            data = request.data
            print('data request for creation of new batch', data)

            data['item'] = item_id

            serializer = self.serializer_class(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                print('error', serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print('error', e)
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # @action(detail=True, url_path='batch=<str:batch_id>', methods=['get'])
    @action(detail=True, methods=['get'])
    def retrieve_batch(self, request, item_id=None, batch_id=None):

        try:
            item_batch = self.get_queryset().get(item_id=item_id, batch_id=batch_id)
            print('getting item_batch', item_batch)
            serializer = self.get_serializer(item_batch)
            return Response(serializer.data)
        except ItemBatch.DoesNotExist:
            raise Http404




class ItemDetailForReportViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemDetailSerializerForReport

    @action(detail=True, methods=['get'])
    def revieve_item_detail_by_batch_id(self, request, pk=None):
        item_detail = self.get_object()
        serializer = self.get_serializer(item_detail)
        return Response(serializer.data)

class ItemFilter(django_filters.FilterSet):
    item_id = django_filters.CharFilter(field_name='id', lookup_expr='icontains')
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    type = django_filters.CharFilter(field_name='type__name', lookup_expr='icontains')
    category = django_filters.CharFilter(field_name='type__category__name', lookup_expr='icontains')
   
    class Meta:
        model = Item
        fields = ['item_id', 'name','category','type']

#example- http://localhost:8000/api/products/?detail=1    
class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializerForUser
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_class = ItemFilter
    pagination_class = StandardResultsSetPagination

    def get_serializer_class(self):
        detail_flag = self.request.query_params.get('detail', '1')
        if detail_flag == '1':
            return ItemSerializerForUser
        elif detail_flag == '2':
            return ItemWithStockInfoSerializer
        elif detail_flag == '3':
            return ItemDetailWithBatchStockInfoSerializer
        return ItemSerializerForUser
    
    def get_paginate_queryset(self, queryset):
        page_size = self.request.query_params.get('page_size', None)
        if page_size:
            try:
                page_size = int(page_size)
                self.pagination_class.page_size = min(page_size, self.pagination_class.max_page_size)
            except ValueError:
                pass
        return super().paginate_queryset(queryset)
    
 

    def list(self, request, *args, **kwargs):
        print('returning list of items')
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)  # Use the paginate_queryset method
     
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)
        return Response(serializer.data)




    def retrieve(self, request, *args, **kwargs):
        print('retrieve method called')
        instance = self.get_object()
        print('instance', instance)
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(instance)
        return Response(serializer.data)
# http://localhost:8000/api/products/?detail=3&page_size=20