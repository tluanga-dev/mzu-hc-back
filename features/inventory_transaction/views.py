from rest_framework import viewsets,generics
from rest_framework.response import Response
from features.item.models import Item



from features.organisation_section.models import OrganisationSection
from features.organisation_section.serializers import OrganisationSectionSerializer
from .models import IndentInventoryTransaction, InventoryTransactionItem, IssueItemInventoryTransaction
from .serializers import IndentInventoryTransactionSerializer, InventoryTransactionItemSerializer, IssueItemInventoryTransactionSerializer, ItemTransactionDetailSerializer 

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
    
class IssueItemInventoryTransactionViewSet(viewsets.ModelViewSet):
    queryset = IssueItemInventoryTransaction.objects.all()
    serializer_class = IssueItemInventoryTransactionSerializer

    def get_queryset(self):
        queryset = IssueItemInventoryTransaction.objects.all()
        issue_to = self.request.query_params.get('issue_to', None)
        issue_date = self.request.query_params.get('issue_date', None)
        issue_date_from = self.request.query_params.get('issue_date_from', None)
        issue_date_to = self.request.query_params.get('issue_date_to', None)

        if issue_to is not None:
            
            organisation_section = OrganisationSection.objects.get(code=issue_to)
            if organisation_section is not None:
                queryset = queryset.filter(issue_to=organisation_section)
      
        
        if issue_date is not None:
            queryset = queryset.filter(issue_date__exact=issue_date)

        if issue_date_from is not None and issue_date_to is not None:
            
            queryset = queryset.filter(issue_date__gte=issue_date_from, issue_date__lte=issue_date_to)

        return queryset
    
    # ------Item Transaction Details
    # 1) Item Detail Information
    # 2) Item Transaction Information - list all transaction where the item is involved
    # 3) Item Stock Information
# class ItemTransactionsView(viewsets.ModelViewSet):
#     queryset = Item.objects.all()
#     serializer_class = ItemSerializer
#     @action(detail=True, url_path='')
#     def retrieve(self, request, *args, **kwargs):
#         instance = self.get_object()
#         serializer = self.get_serializer(instance)

#         # Get the related InventoryTransactionItem instances
#         transactions = InventoryTransactionItem.objects.filter(item=instance)
#         transactions_serializer = InventoryTransactionItemSerializer(transactions, many=True)

#             # Return the item data, item_stock_info, and transactions in the response
#         return Response({
#                 'item': serializer.data,
#                 'item_stock_info': instance.item_stock_info,
#                 'transactions': transactions_serializer.data
#         })


class ItemTransactionsView(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemTransactionDetailSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
