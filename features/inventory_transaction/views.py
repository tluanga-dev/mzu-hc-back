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
        supplyOrderDate = self.request.query_params.get('supplyOrderDate', None)
        supplyOrderDateFrom = self.request.query_params.get('supplyOrderDateFrom', None)
        supplyOrderDateTo = self.request.query_params.get('supplyOrderDateTo', None)

        if supplyOrderNo is not None:
            queryset = queryset.filter(supplyOrderNo=supplyOrderNo)
        if supplier is not None:
            queryset = queryset.filter(supplier=supplier)
        if supplyOrderDate is not None:
            queryset = queryset.filter(supplyOrderDate__exact=supplyOrderDate)
        if supplyOrderDateFrom is not None and supplyOrderDateTo is not None:
            queryset = queryset.filter(supplyOrderDate__gte=supplyOrderDateFrom, supplyOrderDate__lte=supplyOrderDateTo)

        return queryset
    
