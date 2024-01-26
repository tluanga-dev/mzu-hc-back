from django.db import models

from features.item.item_batch.models import ItemBatch
class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('indent', 'Indent'),
        ('dispense', 'Dispense'),
        ('dispose', 'Dispose'),
        ('itemReturnToSupplier', 'ItemReturnToSupplier'),
        ('itemIssue', 'ItemIssue'),
        ('itemIssueReturn', 'ItemIssueReturn'),
        ('itemturnReplacementFromSupplier', 'ItemturnReplacementFromSupplier'),
    ]

    transaction_type = models.CharField(max_length=100, choices=TRANSACTION_TYPES)
    transaction_id = models.CharField(max_length=20, unique=True)
    remarks=models.CharField(max_length=200, unique=True) 
    date_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, default='pending')

    class Meta:
        app_label = 'transaction'


class TransactionItem(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    item_batch = models.ForeignKey(ItemBatch, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'transaction_item'

class IndentTransaction(Transaction):
    requested_quantity = models.IntegerField(blank=True, null=True)
    supplier=models.ForeignKey('supplier.Supplier', on_delete=models.CASCADE)
    supplyOrderNo=models.CharField(max_length=20, unique=True)
    supplyOrderDate=models.DateField()
    dateOfDeliverty=models.DateField()

    class Meta:
        app_label = 'indent_transaction'
      

# class DispenseTransaction(Transaction):
#     patient=models.CharField(max_length=20, unique=True)
#     prescription=models.ForeignKey('prescription.Prescription', on_delete=models.CASCADE)
#     dateOfDispense=models.DateField()

#     class Meta:
#         app_label = 'dispense_transaction'



