# views.py
from django.http import Http404
from rest_framework import status

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from features.utils.convert_date import DateConverter

from features.utils.print_json import print_json_string
from .models import Item, ItemBatch, ItemCategory, ItemType, UnitOfMeasurement
from .serializers import ItemBatchSerializer, ItemCategorySerializer, ItemSerializer, ItemSerializerForUser, ItemTypeSerializer, UnitOfMeasurementSerializer

class UnitOfMeasurementViewSet(viewsets.ModelViewSet):
    queryset = UnitOfMeasurement.objects.all()
    serializer_class = UnitOfMeasurementSerializer

class ItemCategoryViewSet(viewsets.ModelViewSet):
    queryset = ItemCategory.objects.all()
    serializer_class = ItemCategorySerializer

class ItemTypeViewSet(viewsets.ModelViewSet):
    queryset = ItemType.objects.all()
    serializer_class = ItemTypeSerializer

class ItemViewSet(viewsets.ModelViewSet):
    print("ItemViewSet")
    queryset = Item.objects.all()
    serializer_class = ItemSerializerForUser


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
            print('data request for creation of new batch',data)
            
            data['item'] = item_id
            
            serializer = self.serializer_class(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                print('error',serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print('error',e)
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # @action(detail=True, url_path='batch=<str:batch_id>', methods=['get'])
    @action(detail=True, methods=['get'])
    def retrieve_batch(self, request, item_id=None, batch_id=None):
           
            try:
                item_batch = self.get_queryset().get(item_id=item_id, batch_id=batch_id)
                print('getting item_batch',item_batch)
                serializer = self.get_serializer(item_batch)
                return Response(serializer.data)
            except ItemBatch.DoesNotExist:
                raise Http404
