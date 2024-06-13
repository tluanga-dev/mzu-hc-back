from django.utils import timezone
from features.inventory_transaction.inventory_transaction.models import InventoryTransactionItem, ItemStockInfo
from features.item.models import Item, ItemBatch


def generate_dispense_list(inventory_transaction_id,  item_id, required_quantity):
    
    # -----Setup for testing purpose
    required_quantity=6
    
    

    try:
        item = Item.objects.get(id=item_id)
    except Item.DoesNotExist:
        
        return None

    # Fetching non-expired item_batches of an item
    non_expired_batches = ItemBatch.objects.filter(
        item=item,
        date_of_expiry__gte=timezone.now().date()
    )
    

    if not non_expired_batches:
       
        return None
    # --find the latest stock info for item
    latest_item_quantity_in_stock=ItemStockInfo.get_latest_by_item_id(item_id).item_quantity_in_stock
   

    # ---find the latest stock info for each batch
    latest_stock_levels = []
    for batch in non_expired_batches:
        # --check that the batch has stock
        # Get the latest stock info for each batch
        latest_stock_info = ItemStockInfo.get_latest_stock_info_of_item_batch(batch)
        if(latest_stock_info):
            latest_stock_levels.append(latest_stock_info)
  

    # Sort the stock levels by date_of_expiry in ascending order
    sorted_batches_by_date_of_expiry = sorted(latest_stock_levels, key=lambda x: x.item_batch.date_of_expiry)

    # # Sort the stock levels in descending order
    # sorted_batches_by_stock_levels = sorted(latest_stock_levels, key=lambda x: x.item_batch_quantity_in_stock, reverse=True)



    # ------Create the disburesement list
    if required_quantity > latest_item_quantity_in_stock:
        required_quantity = latest_item_quantity_in_stock
    # No need for the else statement, as required_quantity remains the same if it is already less than or equal to latest_item_quantity_in_stock

    total_dispensed = 0

    dispense_inventory_transaction_list = []
    for batch_stock_info in sorted_batches_by_date_of_expiry:
        if total_dispensed >= required_quantity:
            break
        # Check if the batch has enough stock to meet the required quantity
        available_quantity = min(batch_stock_info.item_batch_quantity_in_stock, required_quantity - total_dispensed)
        # print('available_quantity',available_quantity)
        inventory_transaction_item= InventoryTransactionItem(
                inventory_transaction_id=inventory_transaction_id,
                item_batch=batch_stock_info.item_batch,
                quantity=available_quantity
            )
        # print('inventory transaction quantity',inventory_transaction_item.quantity)
        # print('inventory transaction item branch',inventory_transaction_item.item_batch.batch_id)
        # print('inventory transaction item branch',inventory_transaction_item.item_batch.date_of_expiry)
        dispense_inventory_transaction_list.append(
            inventory_transaction_item
        )
        total_dispensed += available_quantity

    return dispense_inventory_transaction_list

    

    #