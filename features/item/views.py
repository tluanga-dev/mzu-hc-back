# views.py
from django.http import Http404
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Item, ItemBatch, ItemCategory, ItemType, UnitOfMeasurement
from .serializers import ItemBatchSerializer, ItemCategorySerializer, ItemSerializer, ItemTypeSerializer, UnitOfMeasurementSerializer

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
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class ItemBatchViewSet(viewsets.ModelViewSet):
    queryset = ItemBatch.objects.all()
    serializer_class = ItemBatchSerializer

    @action(detail=True, url_path='batches')
    def item_batches_by_item_id(self, request, item_id=None):
        """
        Retrieve all item batches associated with a specific item ID.

        Args:
            request (HttpRequest): The HTTP request object.
            item_id (int): The ID of the item.

        Returns:
            Response: The serialized data of the item batches.
        """
        item_batches = self.get_queryset().filter(item_id=item_id)
       
        serializer = self.get_serializer(item_batches, many=True)
        return Response(serializer.data)
    

    @action(detail=False, url_path='batch=<uuid:batch_id>', methods=['get'])
    def retrieve_batch(self, request, item_id=None, batch_id=None):
            """
            Retrieve a specific item batch.

            Args:
                request (HttpRequest): The HTTP request object.
                item_id (str): The ID of the item.
                batch_id (str): The ID of the batch.

            Returns:
                Response: The serialized data of the item batch.

            Raises:
                Http404: If the item batch does not exist.
            """
            try:
                item_batch = self.get_queryset().get(item_id=item_id, id=batch_id)
                serializer = self.get_serializer(item_batch)
                return Response(serializer.data)
            except ItemBatch.DoesNotExist:
                raise Http404
