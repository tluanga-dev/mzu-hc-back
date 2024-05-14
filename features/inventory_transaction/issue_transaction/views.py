from features.inventory_transaction.issue_transaction.models import IssueItemInventoryTransaction
from rest_framework import viewsets

from features.inventory_transaction.issue_transaction.serializers import IssueItemInventoryTransactionSerializer
from features.organisation_unit.models import OrganisationUnit

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
            
            organisation_section = OrganisationUnit.objects.get(code=issue_to)
            if organisation_section is not None:
                queryset = queryset.filter(issue_to=organisation_section)
      
        
        if issue_date is not None:
            queryset = queryset.filter(issue_date__exact=issue_date)

        if issue_date_from is not None and issue_date_to is not None:
            
            queryset = queryset.filter(issue_date__gte=issue_date_from, issue_date__lte=issue_date_to)

        return queryset