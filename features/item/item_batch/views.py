from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from features.item.item_batch.models import ItemBatch
from features.item.item_batch.serializers import ItemBatchSerializer

class ItemBatchViewSet(viewsets.ModelViewSet):
    queryset = ItemBatch.objects.all()
    serializer_class = ItemBatchSerializer

    @action(detail=True, url_path='batches')
    def item_batches_by_item_id(self, request, item_id=None):
        item_batches = self.get_queryset().filter(item_id=item_id)
       
        serializer = self.get_serializer(item_batches, many=True)
        return Response(serializer.data)