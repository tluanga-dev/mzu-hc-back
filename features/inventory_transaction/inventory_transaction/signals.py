from django.dispatch import receiver
from django.db.models.signals import post_save

from features.inventory_transaction.inventory_transaction.models import InventoryTransaction, InventoryTransactionItem, ItemStockInfo

@receiver(post_save, sender=InventoryTransactionItem)
def post_save_inventory_transaction_item(sender, instance, created, **kwargs):
   
    if created:
        # --get the latest item stock info
        item=instance.item_batch.item
        previous_quantity_inhand = 0
        previous_stock_info=ItemStockInfo.objects.filter(item=item).last()
        if previous_stock_info is not None:
            previous_quantity_inhand = previous_stock_info.quantity
        # else:
        #     print(len(ItemStockInfo.objects.filter(item=item)))
       
        # print('item:', item_stock_info)
        transaction_type=instance.inventory_transaction.inventory_transaction_type
        if(transaction_type==InventoryTransaction.TransactionTypes.INDENT):

           ItemStockInfo.objects.create(
                item=item,
                quantity=previous_quantity_inhand+instance.quantity,
                inventory_transaction_item=instance,
            )
        
            
        elif (
            transaction_type == InventoryTransaction.TransactionTypes.ITEM_ISSUE or 
            transaction_type == InventoryTransaction.TransactionTypes.DISPENSE
            ):      
            if(previous_quantity_inhand<instance.quantity):
                # print('previous quantity inhand:', previous_quantity_inhand)
                raise ValueError('Item stock is less than the quantity to be issued')
            else:
                new_item_stock_info=ItemStockInfo.objects.create(
                item=item,
                quantity=previous_quantity_inhand-instance.quantity,
                inventory_transaction_item=instance,

                )
                # print('new_item_stock_info:', new_item_stock_info.quantity)
 
