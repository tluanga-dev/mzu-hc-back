from datetime import timezone
import datetime
from django.db import models
from features.item.item_batch.models import ItemBatch

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class InventoryTransaction(models.Model):
    inventory_transaction_id = models.CharField(max_length=20, unique=True)
    remarks=models.CharField(max_length=200, unique=False, blank=True, null=True) 
    date_time = models.DateTimeField(auto_now_add=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    class Meta:
        app_label = 'inventory_transaction'
        

class InventoryTransactionItem(models.Model):
    inventory_transaction = models.ForeignKey(
        InventoryTransaction, 
        on_delete=models.CASCADE, 
    related_name='inventorytransactionitem_set'
    )
    item_batch = models.ForeignKey(ItemBatch, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False, blank=False)
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'inventory_transaction'

class IndentInventoryTransaction(InventoryTransaction):
    supplier=models.ForeignKey('supplier.Supplier', on_delete=models.CASCADE)
    supplyOrderNo=models.CharField(max_length=20, unique=True)
    supplyOrderDate=models.DateField()
    dateOfDeliverty=models.DateField()


    def __str__(self):
       
        return f'IndentInventoryTransaction {self.inventory_transaction_id} - {self.inventory_transaction_type} - {self.remarks} - {self.date_time} - {self.status} - {self.supplyOrderNo} - {self.supplyOrderDate} - {self.dateOfDeliverty}'

    
    class Meta:
        app_label = 'inventory_transaction'
      




