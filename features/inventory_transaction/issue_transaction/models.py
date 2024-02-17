import uuid
from django.db import models

from features.inventory_transaction.inventory_transaction.models import InventoryTransaction
from features.organisation_section.models import OrganisationSection


class IssueItemInventoryTransaction(InventoryTransaction):
    issue_date=models.DateField(blank=False, null=False)
    item_receiver=models.CharField(max_length=200, blank=False, null=False)
    issue_to=models.ForeignKey(
        OrganisationSection, 
        on_delete=models.CASCADE, 
        related_name='issue_to',
        null=False,
        blank=False
    )
    
    def save(self, *args, **kwargs):
        if self.pk is None:
            self.inventory_transaction_type = self.TransactionTypes.ITEM_ISSUE
        super().save(*args, **kwargs)
   
    class Meta:
        app_label = 'issue_transaction'
