
from django.db import models
from django.utils.translation import gettext_lazy as _
from features.base.time_stamped_abstract_class import TimeStampedAbstractModelClass
from features.id_manager.models import IdManager
from features.item.models import Item, ItemBatch


import logging

# Configure logging
logger = logging.getLogger(__name__)


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



class ItemStockInfo(TimeStampedAbstractModelClass):
    
    inventory_transaction_item = models.OneToOneField(InventoryTransactionItem, on_delete=models.CASCADE, related_name='item_batch_stock_info')
    inventory_transaction_type = models.CharField(max_length=100, choices=InventoryTransaction.TransactionTypes.choices)
    item_name=models.CharField(max_length=255)
    item=models.ForeignKey(Item, on_delete=models.CASCADE, related_name='item_batch_stock_info') 
    item_batch_name=models.CharField(max_length=255)
    item_batch = models.ForeignKey(ItemBatch, on_delete=models.CASCADE, related_name='item_batch_stock_info') 
    # --quantity for that transaction
    quantity = models.PositiveIntegerField(null=False, blank=False)
    # --latest quantity in stock after the transaction for the item-including all batches
    item_quantity_in_stock = models.PositiveIntegerField(null=False, blank=False)
    # --latest quantity in stock after the transaction for the item batch
    item_batch_quantity_in_stock = models.PositiveIntegerField(null=False, blank=False)

    class Meta:
        app_label = 'inventory_transaction'

    @classmethod
    def get_latest_by_item_id(cls, item_id):
        try:
            # Ensure the query is correctly capturing the latest item stock info
            # Using '-created_at' to ensure we get the most recent record first
            data = cls.objects.filter(item=item_id).order_by('created_at').last()
            # if data:
            #     print(f'Successfully found latest stock info for item_id {item_id}: {data}')
            # else:
            #     print(f'No stock info found for item_id {item_id}')
            return data
        except Exception as e:
            print(f'Error retrieving stock info for item_id {item_id}: {str(e)}')
            return None
    
    @classmethod
    def get_latest_by_item_batch_id(cls, item_batch_id):
        # Assuming ItemBatch has a direct link to Item which needs to be confirmed
        return cls.objects.filter(item_batch=item_batch_id).order_by('created_at').last()
    
    @classmethod
    def get_latest_stock_info_of_item_batch(cls, item_batch_id):
        try:
            data = cls.objects.filter(item_batch=item_batch_id).order_by('created_at').last()
            if data:
                # print(f'Successfully found latest stock info for item_batch_id {item_batch_id}: {data}')
                return data
                
            else:
                # print(f'No stock info found for item_batch_id {item_batch_id}')
                return None
            
        except Exception as e:
            print(f'Error retrieving stock info for item_batch_id {item_batch_id}: {str(e)}')
            return None


     
  


