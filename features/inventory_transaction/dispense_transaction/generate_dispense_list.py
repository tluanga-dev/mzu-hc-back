from django.utils import timezone
from features.inventory_transaction.inventory_transaction.models import InventoryTransactionItem, ItemStockInfo
from features.item.models import Item, ItemBatch
from features.item.serializers import ItemBatchSerializer

def generate_dispense_list( item_id, required_quantity):
    print('item_id', item_id)
    print('required_quantity', required_quantity)
    try:
        item = Item.objects.get(id=item_id)
    except Item.DoesNotExist:
        print("Item not found")
        return None

    # Fetching non-expired item_batches of an item
    non_expired_batches = ItemBatch.objects.filter(
        item=item,
        date_of_expiry__gte=timezone.now().date()
    )
    # print('\n\n\n non expired batches\n')
    # for batch in non_expired_batches:
    #     print('\n')
    #     print(ItemBatchSerializer(batch).data)
    # print('\n\n')    



    if not non_expired_batches:
        print("No available batches which are not expired found")
        return None
    
    latest_stock_levels = []
    for batch in non_expired_batches:
        # Get the latest stock info for each batch
        latest_stock_info = ItemStockInfo.objects.filter(
            item_batch=batch,
            quantity_in_stock__gt=0
        ).order_by('-id').first()
        if latest_stock_info:
            latest_stock_levels.append(latest_stock_info)

    # Sort the stock levels by date_of_expiry in ascending order
    sorted_batches_by_date_of_expiry = sorted(latest_stock_levels, key=lambda x: x.item_batch.date_of_expiry)

    # Sort the stock levels in descending order
    sorted_batches_by_stock_levels = sorted(latest_stock_levels, key=lambda x: x.quantity_in_stock, reverse=True)
    
    
    # Get the item_stock_infos for the sorted stock levels
    # item_stock_infos = ItemStockInfo.objects.filter(id__in=[stock_level.id for stock_level in sorted_stock_levels])
    
    print('sorted_batches_by_date_of_expiry', sorted_batches_by_date_of_expiry)
    print('sorted_batches_by_stock_levels', sorted_batches_by_stock_levels)
    
    

    # total_dispensed = 0
    # dispense_list = []
    # # Iterate over batches to collect sufficient quantity
    # for item_stock_info in item_stock_infos:
    #     if total_dispensed >= required_quantity:
    #         break
    #     # Check if the batch has enough stock to meet the required quantity
    #     available_quantity = min(item_stock_info.quantity_in_stock, required_quantity - total_dispensed)
    #     dispense_list.append(
    #         InventoryTransactionItem(
    #             item_batch=item_stock_info.item_batch,
    #             quantity=available_quantity
    #         )
    #     )
    #     total_dispensed += available_quantity
    # if total_dispensed < required_quantity:
    #     print("Insufficient total stock to meet the requested quantity")
    # return {
    #     'item': item,
    #     'dispense_batches': dispense_list
    # }


    # Gather batches with available stock that hasn't expired, ordered by expiry date
    # batch with the earliest expiry date is dispensed first
    # batch with the latest expiry date is dispensed last
    # item can have many batches, each with its own stock level
    # in ItemStockInfo there can be many entries
    # of that batch with different stock levels
    # i want to get the entry with the latest stock level of that batch

  

    # Sort the stock levels in descending order
    sorted_stock_levels = sorted(latest_stock_levels, key=lambda x: x.quantity_in_stock, reverse=True)
    # Get the item_stock_infos for the sorted stock levels
    item_stock_infos = ItemStockInfo.objects.filter(id__in=[stock_level.id for stock_level in sorted_stock_levels])
    if not item_stock_infos:
        print("No available batches with stock found")
        return None
    total_dispensed = 0
    # Iterate over batches to collect sufficient quantity
    for item_stock_info in item_stock_infos:
        if total_dispensed >= required_quantity:
            break
        # --- Check if the batch has enough stock to meet the required quantity
        available_quantity = min(item_stock_info.quantity_in_stock, required_quantity - total_dispensed)
        dispense_list = InventoryTransactionItem(
            item_batch=item_stock_info.item_batch,
            quantity=available_quantity
        )
        total_dispensed += available_quantity
    if total_dispensed < required_quantity:
        print("Insufficient total stock to meet the requested quantity")
    return {
        'item': item,
        'dispense_batches': dispense_list
    }

    # Sort the stock levels in descending order
    sorted_stock_levels = sorted(latest_stock_levels, key=lambda x: x.quantity_in_stock, reverse=True)

    # Get the item_stock_infos for the sorted stock levels
    item_stock_infos = ItemStockInfo.objects.filter(id__in=[stock_level.id for stock_level in sorted_stock_levels])

    if not item_stock_infos:
        print("No available batches with stock found")
        return None

    total_dispensed = 0

    # Iterate over batches to collect sufficient quantity
    for item_stock_info in item_stock_infos:
        if total_dispensed >= required_quantity:
            break
        # --- Check if the batch has enough stock to meet the required quantity
        available_quantity = min(item_stock_info.quantity_in_stock, required_quantity - total_dispensed)
        dispense_list = InventoryTransactionItem(
            item_batch=item_stock_info.item_batch,
            quantity=available_quantity
        )
        total_dispensed += available_quantity

    if total_dispensed < required_quantity:
        print("Insufficient total stock to meet the requested quantity")

    return {
        'item': item,
        'dispense_batches': dispense_list
    }
