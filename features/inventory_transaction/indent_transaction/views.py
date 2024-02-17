from rest_framework import viewsets

from features.inventory_transaction.indent_transaction.models import IndentInventoryTransaction
from features.inventory_transaction.indent_transaction.serializers import IndentInventoryTransactionSerializer


class IndentInventoryTransactionViewSet(viewsets.ModelViewSet):
    queryset = IndentInventoryTransaction.objects.all()
    serializer_class = IndentInventoryTransactionSerializer

    def get_queryset(self):
        queryset = IndentInventoryTransaction.objects.all()
        supply_order_no = self.request.query_params.get('supply_order_no', None)
        supplier = self.request.query_params.get('supplier', None)
        supply_order_date = self.request.query_params.get('supply_order_date', None)
        supply_order_dateFrom = self.request.query_params.get('supply_order_dateFrom', None)
        supply_order_dateTo = self.request.query_params.get('supply_order_dateTo', None)

        if supply_order_no is not None:
            queryset = queryset.filter(supply_order_no=supply_order_no)
        if supplier is not None:
            queryset = queryset.filter(supplier=supplier)
        if supply_order_date is not None:
            queryset = queryset.filter(supply_order_date__exact=supply_order_date)
        if supply_order_dateFrom is not None and supply_order_dateTo is not None:
            queryset = queryset.filter(supply_order_date__gte=supply_order_dateFrom, supply_order_date__lte=supply_order_dateTo)

        return queryset