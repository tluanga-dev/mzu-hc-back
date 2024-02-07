from django.dispatch import receiver
from django.db.models.signals import post_save

from .models import InventoryTransaction, InventoryTransactionItem

@receiver(post_save, sender=InventoryTransactionItem)
def post_save_inventory_transaction_item(sender, instance, created, **kwargs):
  
   
    if created:
        item=instance.item_batch.item
        item_stock_info=item.item_stock_info
        # print('item:', item_stock_info)
        transaction_type=instance.inventory_transaction.inventory_transaction_type
        if(transaction_type==InventoryTransaction.TransactionTypes.INDENT):
          
            item_stock_info.quantity+=instance.quantity
            item_stock_info.save()
            
        elif(transaction_type==InventoryTransaction.TransactionTypes.ITEM_ISSUE):
           
       
            item=instance.item_batch.item
            item_stock_info=item.item_stock_info
            if(item_stock_info.quantity<instance.quantity):
               
                raise ValueError('Item stock is less than the quantity to be issued')
            else:
                item_stock_info.quantity-=instance.quantity
                item_stock_info.save()
        
