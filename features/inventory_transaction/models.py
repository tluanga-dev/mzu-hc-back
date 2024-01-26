from django.db import models

from features.item.item_batch.models import ItemBatch


class InventoryTransaction(models.Model):

    INDENT = 'indent'
    DISPENSE = 'dispense'
    DISPOSE = 'dispose'
    ITEM_RETURN_TO_SUPPLIER = 'itemReturnToSupplier'
    ITEM_ISSUE = 'itemIssue'
    ITEM_ISSUE_RETURN = 'itemIssueReturn'
    ITEM_TURN_REPLACEMENT_FROM_SUPPLIER = 'itemturnReplacementFromSupplier'


    TRANSACTION_TYPES = [
        ('indent', 'Indent'),
        ('dispense', 'Dispense'),
        ('dispose', 'Dispose'),
        ('itemReturnToSupplier', 'ItemReturnToSupplier'),
        ('itemIssue', 'ItemIssue'),
        ('itemIssueReturn', 'ItemIssueReturn'),
        ('itemturnReplacementFromSupplier', 'ItemturnReplacementFromSupplier'),
    ]

    inventory_transaction_type = models.CharField(max_length=100, choices=TRANSACTION_TYPES)
    iventory_transaction_id = models.CharField(max_length=20, unique=True)
    remarks=models.CharField(max_length=200, unique=True) 
    date_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, default='pending')

    class Meta:
        app_label = 'inventory_transaction'


class InventoryTransactionItem(models.Model):
    inventory_transaction = models.ForeignKey(InventoryTransaction, on_delete=models.CASCADE)
    item_batch = models.ForeignKey(ItemBatch, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'inventory_transaction'

class IndentInventoryTransaction(InventoryTransaction):
    quantity = models.IntegerField(blank=False, null=False)
    supplier=models.ForeignKey('supplier.Supplier', on_delete=models.CASCADE)
    supplyOrderNo=models.CharField(max_length=20, unique=True)
    supplyOrderDate=models.DateField()
    dateOfDeliverty=models.DateField()

    class Meta:
        app_label = 'inventory_transaction'
      




