

from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import IndentInventoryTransaction, InventoryTransactionItem
from .serializers import IndentInventoryTransactionSerializer, InventoryTransactionItemSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import IndentInventoryTransaction
from .serializers import IndentInventoryTransactionSerializer

class IndentInventoryTransactionViewSet(viewsets.ModelViewSet):
    queryset = IndentInventoryTransaction.objects.all()
    serializer_class = IndentInventoryTransactionSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)