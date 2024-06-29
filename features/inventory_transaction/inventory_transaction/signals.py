from django.dispatch import receiver
from django.db.models.signals import post_save

from features.inventory_transaction.inventory_transaction.models import InventoryTransaction, InventoryTransactionItem, ItemStockInfo
from features.item.models import Item
from features.item.serializers.item_with_batch_stock_info_serializer import ItemDetailWithBatchStockInfoSerializer
from django.core.cache import cache

@receiver(post_save, sender=InventoryTransactionItem)
def post_save_inventory_transaction_item(sender, instance, created, **kwargs):
    if created:
        item_batch = instance.item_batch
        item=item_batch.item
        

        # -----------------Get the previous stock info for the item
        item_previous_stock_info = ItemStockInfo.get_latest_by_item_id(item.id)

        # print('item_previous_stock_info', item_previous_stock_info)


        item_previous_quantity_in_stock = item_previous_stock_info.item_quantity_in_stock if item_previous_stock_info else 0

        # print('previous_quantity_instock', item_previous_quantity_in_stock)


        # -----------------Get the Previous stock info for the item batch

        item_batch_previous_stock_info = ItemStockInfo.get_latest_stock_info_of_item_batch(instance.item_batch)
        item_batch_previous_quantity_in_stock = item_batch_previous_stock_info.item_batch_quantity_in_stock if item_batch_previous_stock_info else 0

        # print('previous_quantity_instock', item_previous_quantity_in_stock)
        
        transaction_type = instance.inventory_transaction.inventory_transaction_type
        # print(transaction_type)
        if transaction_type == InventoryTransaction.TransactionTypes.INDENT:
            ItemStockInfo.objects.create(
                item_batch_name=item_batch.batch_id,
                item_batch=item_batch,
                item_name=item.name,
                item=item,
                inventory_transaction_type=transaction_type,
                item_quantity_in_stock=item_previous_quantity_in_stock + instance.quantity,
                item_batch_quantity_in_stock=item_batch_previous_quantity_in_stock+ instance.quantity,
                quantity= instance.quantity,
                inventory_transaction_item=instance,
            )
        elif transaction_type in [InventoryTransaction.TransactionTypes.ITEM_ISSUE, InventoryTransaction.TransactionTypes.DISPENSE]:
            # print('signal triggered for Dispanese')
            if item_previous_quantity_in_stock < instance.quantity:
                raise ValueError('Item stock is less than the quantity to be issued')
            # print('batch_id', item_batch.batch_id)
            # print('item_previous_quantity_in_stock', item_previous_quantity_in_stock)
            # print('instance.quantity', instance.quantity)
            # print('item_previous_quantity_in_stock - instance.quantity', item_previous_quantity_in_stock - instance.quantity)
            item_stock_info= ItemStockInfo.objects.create(
                item_batch_name=item_batch.batch_id,
                item_batch=item_batch,
                item_name=item.name,
                inventory_transaction_type=transaction_type,
                item=item,
                quantity= instance.quantity,
                item_quantity_in_stock=item_previous_quantity_in_stock - instance.quantity,
                item_batch_quantity_in_stock=item_batch_previous_quantity_in_stock -instance.quantity,
                inventory_transaction_item=instance,
            )
            item_stock_info.save()
        items=Item.objects.all()
        serializer=ItemDetailWithBatchStockInfoSerializer(items, many=True)
        cache.set('item_detail_with_batch_stock_info_cache_key', serializer.data)