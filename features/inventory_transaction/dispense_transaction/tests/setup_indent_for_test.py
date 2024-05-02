from datetime import date
from features.inventory_transaction.indent_transaction.models import IndentInventoryTransaction
from features.inventory_transaction.indent_transaction.serializers import IndentInventoryTransactionSerializer
from features.inventory_transaction.inventory_transaction.models import InventoryTransaction, InventoryTransactionItem
from features.item.models import Item, ItemBatch
from features.supplier.models import Supplier


def setup_indent_for_test(item_type, unit_of_measurement):
    IndentInventoryTransaction.objects.all().delete()
    InventoryTransactionItem.objects.all().delete()
    Item.objects.all().delete()
    Supplier.objects.all().delete()
    item = Item.objects.create(
            name="Test Item",
            description="Test Description",
            type=item_type,
            unit_of_measurement=unit_of_measurement,
            is_active=True
        )
    item.save()
   

    supplier = Supplier.objects.create(
            name='Test Supplier',
            contact_no=1234567890,
            email='test@gmail.com',
            address='Test Address',
            is_active=True

    )
    supplier.save()
    item_batch1 = ItemBatch.objects.create(
            batch_id='B1',
            description='Test Batch 1',
           date_of_expiry=date(2025, 12, 12),
            item=item
        )
    item_batch2 = ItemBatch.objects.create(
            batch_id='B2',
            description='Test Batch 2',
            date_of_expiry=date(2024, 12, 12),
            item=item
    )
    item_batch2.save()

    indent_transaction_data = {
            'inventory_transaction_type': InventoryTransaction.TransactionTypes.INDENT,
            'supplier': supplier.id,
            'supply_order_no': 'SO1/992-223/222\2',
            'supply_order_date': '01-01-2022',
            'date_of_delivery': '03-01-2022',
            'remarks': None,
            'inventory_transaction_item_set': [
                {
                    'item_batch': item_batch1.id,
                    'quantity': 10,
                    'is_active': True,
                    'inventory_transaction_type': InventoryTransaction.TransactionTypes.INDENT,

                },
                {
                    'item_batch': item_batch2.id,
                    'quantity': 5,
                    'is_active': True,
                    'inventory_transaction_type': InventoryTransaction.TransactionTypes.INDENT,

                }
            ],


        }
    IndentInventoryTransaction.objects.all().delete()
    serializer = IndentInventoryTransactionSerializer(
            data=indent_transaction_data)

    if (serializer.is_valid()):
            serializer.save()
            print('indent transaction setup completeted')
            return {'serializer_data': serializer.data, 'medicine': item}
    else:
            print('serializer is not valid')
            print(serializer.errors)
