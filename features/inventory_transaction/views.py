from rest_framework import viewsets
from .models import IndentInventoryTransaction
from .serializers import IndentInventoryTransactionSerializer

class IndentInventoryTransactionViewSet(viewsets.ModelViewSet):
    queryset = IndentInventoryTransaction.objects.all()
    serializer_class = IndentInventoryTransactionSerializer