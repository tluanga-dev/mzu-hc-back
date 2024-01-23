from django.db import models

from features.transaction.base.transaction import Transaction

# Create your models here.
class IndentTransaction(Transaction):
    requested_quantity = models.IntegerField(blank=True, null=True)
    supplier_details = models.CharField(max_length=100, blank=True)