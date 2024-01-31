from rest_framework import viewsets
from .models import IndentInventoryTransaction
from .serializers import IndentInventoryTransactionSerializer

class IndentInventoryTransactionViewSet(viewsets.ModelViewSet):
    queryset = IndentInventoryTransaction.objects.all()
    serializer_class = IndentInventoryTransactionSerializer

    def get_queryset(self):
        queryset = IndentInventoryTransaction.objects.all()
        supplyOrderNo = self.request.query_params.get('supplyOrderNo', None)
        supplier = self.request.query_params.get('supplier', None)

        if supplyOrderNo is not None:
            queryset = queryset.filter(supplyOrderNo=supplyOrderNo)
        if supplier is not None:
            queryset = queryset.filter(supplier=supplier)
        
         # Print the number of related InventoryTransactionItem instances for each IndentInventoryTransaction
        # for transaction in queryset:
        #     print(transaction.inventorytransactionitem_set.count())

        return queryset