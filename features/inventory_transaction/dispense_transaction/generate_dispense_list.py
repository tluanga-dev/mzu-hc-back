from django.utils import timezone
from django.db.models import Q
from features.inventory_transaction.inventory_transaction.models import ItemStockInfo
from features.item.models import Item, ItemBatch  # Ensure proper import paths

def generate_dispense_list(item_id, required_quantity):
  
    try:
        item = Item.objects.get(id=item_id)
    except Item.DoesNotExist:
        print("Item not found")
        return None

    # Gather batches with available stock that hasn't expired, ordered by expiry date
    batches = ItemBatch.objects.filter(
        item=item,
        quantity_in_stock__gt=0,  # Only consider batches with stock
        date_of_expiry__gte=timezone.now().date()  # Exclude expired batches
    ).order_by('date_of_expiry')

    if not batches:
        print("No available batches with stock found")
        return None

    dispense_list = []
    total_dispensed = 0

    # Iterate over batches to collect sufficient quantity
    for batch in batches:
        if total_dispensed >= required_quantity:
            break
        quantity_available_in_item_batch=ItemStockInfo.get_latest_by_item_batch_id(batch.id).quantity_in_stock
        available_quantity = min(quantity_available_in_item_batch, required_quantity - total_dispensed)
        dispense_list.append({
            'item_batch': batch,
            'quantity': available_quantity
        })
        total_dispensed += available_quantity

    if total_dispensed < required_quantity:
        print("Insufficient total stock to meet the requested quantity")

    return {
        'item': item,
        'dispense_batches': dispense_list
    }
