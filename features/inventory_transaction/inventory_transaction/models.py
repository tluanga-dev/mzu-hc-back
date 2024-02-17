
from django.db import models
from django.utils.translation import gettext_lazy as _
from features.base.time_stamped_abstract_class import TimeStampedAbstractModelClass
from features.id_manager.models import IdManager
from features.item.models import Item, ItemBatch


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
 
    class Meta:
        app_label = 'inventory_transaction'


# --every inventory transaction item will update this
# --this will be used to calculate the stock of the item
class ItemStockInfo(TimeStampedAbstractModelClass):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='item_stock_info') 
    inventory_transaction_item = models.OneToOneField(InventoryTransactionItem, on_delete=models.CASCADE, related_name='item_stock_info')
    quantity = models.PositiveIntegerField(null=False, blank=False)

    class Meta:
        app_label = 'inventory_transaction'

    @classmethod
    def get_latest_by_item_id(cls, item_id):
        return cls.objects.filter(item_id=item_id).last()


