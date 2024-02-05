from django.db import models
from django.utils.translation import gettext_lazy as _
from features.base.time_stamped_abstract_class import TimeStampedAbstractModelClass
from features.id_manager.models import IdManager


from features.item.models import ItemBatch

class InventoryTransaction(TimeStampedAbstractModelClass):
    class TransactionTypes(models.TextChoices):
        INDENT = 'indent', _('Indent')
        DISPENSE = 'dispense', _('Dispense')
        DISPOSE = 'dispose', _('Dispose')
        ITEM_RETURN_TO_SUPPLIER = 'itemReturnToSupplier', _('ItemReturnToSupplier')
        ITEM_ISSUE = 'itemIssue', _('ItemIssue')
        ITEM_ISSUE_RETURN = 'itemIssueReturn', _('ItemIssueReturn')
        ITEM_TURN_REPLACEMENT_FROM_SUPPLIER = 'itemturnReplacementFromSupplier', _('ItemturnReplacementFromSupplier')

    CODES = {
        'indent': 'INDT',
        'dispense': 'DISP',
        'dispose': 'DISO',
        'itemReturnToSupplier': 'IRTS',
        'itemIssue': 'ITIS',
        'itemIssueReturn': 'IIRN',
        'itemturnReplacementFromSupplier': 'ITRS',
        }

    inventory_transaction_type = models.CharField(max_length=100, choices=TransactionTypes.choices)

    inventory_transaction_id = models.CharField(max_length=100,  editable=False)
    
    date_time = models.DateTimeField(auto_now_add=True)
    remarks = models.CharField(max_length=200, blank=True, null=True) 


    def generate_inventory_transaction_id(self):
        if self.inventory_transaction_type in self.TransactionTypes.values:
            self.inventory_transaction_id = IdManager.generateId(prefix=self.inventory_transaction_type)
        else:
            raise ValueError("Invalid inventory_transaction_type")

    def save(self, *args, **kwargs):
        self.generate_inventory_transaction_id()
            
        super().save(*args, **kwargs)
   

    class Meta:
        app_label = 'inventory_transaction'

class InventoryTransactionItem(TimeStampedAbstractModelClass):
    inventory_transaction = models.ForeignKey(
        InventoryTransaction, 
        on_delete=models.CASCADE, 
        related_name='inventory_transaction_item_set'
    )
    item_batch = models.ForeignKey(ItemBatch, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False, blank=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        app_label = 'inventory_transaction'

class IndentInventoryTransaction(InventoryTransaction):
    supplier=models.ForeignKey('supplier.Supplier', on_delete=models.CASCADE)
    supply_order_no=models.CharField(max_length=20, unique=True)
    supply_order_date=models.DateField()
    date_of_delivery=models.DateField()

   
    class Meta:
        app_label = 'inventory_transaction'

