from datetime import date
from django.test import TestCase
from features.base.base_test_setup_class import BaseTestCase
from features.item.item.models import Item

from features.supplier.models import Supplier
from .models import  InventoryTransactionItem, IndentInventoryTransaction, ItemBatch
from .serializers import IndentInventoryTransactionSerializer

class IndentInventoryTransactionSerializerTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.item = Item.objects.create(
            name="Test Item",
            description="Test Description",
            type=self.item_type,
            unit_of_measurement=self.unit_of_measurement,
            is_active=True
        )
        self.item.save()

        self.supplier = Supplier.objects.create(
            name='Test Supplier',
            contact_no='1234567890',
            email='test@gmail.com',
            address='Test Address',
            is_active=True
        )
        self.supplier.save()
        self.item_batch1=ItemBatch.objects.create(
            batch_id='B2',
            description='Test Batch 1',
            date_of_expiry=date.today(),
            item=self.item
        )
        self.item_batch1.save()

        self.indent_transaction_data = {
            'inventory_transaction_type': 'indent',
            'inventory_transaction_id': 'INDENT1',
            'status': 'pending',
            'supplier': self.supplier.id,
            'supplyOrderNo': 'SO1',
            'supplyOrderDate': '2022-01-01',
            'dateOfDeliverty': '2022-01-01',
            'remarks': None,
            'inventory_transaction_item': [
                {
                    'item_batch': self.item_batch1.id,
                    'quantity': 10,
                    'is_active': True
                },
                {
                    'item_batch': self.item_batch1.id,
                    'quantity': 5,
                    'is_active': True
                }
            ]
        }
        # print('\n---------------\n')
        # print(self.indent_transaction_data)
        # print('\n---------------\n')

    def test_create_indent_inventory_transaction(self):
        print('\n-------test_create_indent_inventory_transaction------- ')
        IndentInventoryTransaction.objects.all().delete()
        serializer = IndentInventoryTransactionSerializer(data=self.indent_transaction_data)
        
        self.assertTrue(serializer.is_valid())
        
        serializer.save()

        indent_transaction = IndentInventoryTransaction.objects.get(inventory_transaction_id='INDENT1')
        self.assertEqual(indent_transaction.inventory_transaction_type, 'indent')
        self.assertEqual(indent_transaction.status, 'pending')
        self.assertEqual(indent_transaction.supplier, self.supplier)
        self.assertEqual(indent_transaction.supplyOrderNo, 'SO1')

        transaction_items = InventoryTransactionItem.objects.filter(inventory_transaction=indent_transaction)
        self.assertEqual(transaction_items.count(), 2)
        print('-------End of test_create_indent_inventory_transaction-------\n ')

    # def test_retrieve_indent_inventory_transaction(self):
    #     serializer = IndentInventoryTransactionSerializer(data=self.indent_transaction_data)
    #     if not serializer.is_valid():
    #         print('-------serializer errors------- ')
    #         print(serializer.errors)
    #         print('-------serializer data------- ')
    #     self.assertTrue(serializer.is_valid())
    #     serializer.save()

    #     indent_transaction = IndentInventoryTransaction.objects.get(inventory_transaction_id='INDENT1')
    #     serializer = IndentInventoryTransactionSerializer(indent_transaction)

    #     expected_data = self.indent_transaction_data.copy()
    #     expected_data['id'] = indent_transaction.id
    #     expected_data['supplier'] = {
    #         'id': self.supplier.id,
    #         'name': 'Test Supplier',
    #         'contact_no': '1234567890',
    #         'email': 'test@gmail.com',
    #         'address': 'Test Address',
    #         'remarks': None,
    #         'is_active': True
    #     }
    #     expected_data['date_time'] = indent_transaction.date_time.strftime('%d-%m-%Y %H:%M')
    #     expected_data['inventory_transaction_item'] = [
    #         {
    #             'id': item.id,
    #             'inventory_transaction': indent_transaction.id,
    #             'item_batch': item.item_batch.id,
    #             'quantity': item.quantity,
    #             'is_active': item.is_active,
    #             'created_on': item.created_on.isoformat(),
    #             'updated_on': item.updated_on.isoformat(),
    #         } for item in InventoryTransactionItem.objects.filter(inventory_transaction=indent_transaction)
    #     ]

    #     self.assertEqual(serializer.data, expected_data)