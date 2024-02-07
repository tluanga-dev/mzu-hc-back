from rest_framework import viewsets

from features.organisation_section.models import OrganisationSection
from features.organisation_section.serializers import OrganisationSectionSerializer
from .models import IndentInventoryTransaction, IssueItemInventoryTransaction
from .serializers import IndentInventoryTransactionSerializer, IssueItemInventoryTransactionSerializer

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
    
