from django.dispatch import receiver
from django.db.models.signals import post_save

from features.inventory_transaction.inventory_transaction.models import InventoryTransaction, InventoryTransactionItem, ItemStockInfo
from features.item.serializers import ItemSerializer

@receiver(post_save, sender=InventoryTransactionItem)
def post_save_inventory_transaction_item(sender, instance, created, **kwargs):
    if created:
        item_batch = instance.item_batch
        item=item_batch.item
        
        previous_stock_info = ItemStockInfo.get_latest_by_item_id(item.id)

        # print('previous_stock_info', previous_stock_info)

        previous_quantity_in_stock = previous_stock_info.quantity_in_stock if previous_stock_info else 0

        # print('previous_quantity_inhand', previous_quantity_inhand)
        
        transaction_type = instance.inventory_transaction.inventory_transaction_type
        print(transaction_type)
        if transaction_type == InventoryTransaction.TransactionTypes.INDENT:
            ItemStockInfo.objects.create(
                item_batch_name=item_batch.batch_id,
                item_batch=item_batch,
                item_name=item.name,
                item=item,
                inventory_transaction_type=transaction_type,
                quantity_in_stock=previous_quantity_in_stock + instance.quantity,
                quantity= instance.quantity,
                inventory_transaction_item=instance,
            )
        elif transaction_type in [InventoryTransaction.TransactionTypes.ITEM_ISSUE, InventoryTransaction.TransactionTypes.DISPENSE]:
            if previous_quantity_in_stock < instance.quantity:
                raise ValueError('Item stock is less than the quantity to be issued')
            ItemStockInfo.objects.create(
                item_batch_name=item_batch.batch_id,
                item_batch=item_batch,
                item_name=item.name,
                inventory_transaction_type=transaction_type,
                item=item,
                quantity=previous_quantity_inhand - instance.quantity,
                inventory_transaction_item=instance,
            )