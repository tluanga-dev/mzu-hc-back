from datetime import date
import os
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
            'inventorytransactionitem_set': [
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

    # def test_create_indent_inventory_transaction(self):
    #     # print('\n-------test_create_indent_inventory_transaction------- ')
    #     IndentInventoryTransaction.objects.all().delete()
    #     # print('------data input to serializer------')
    #     # print(self.indent_transaction_data)
    #     # print('\n\n')
    #     serializer = IndentInventoryTransactionSerializer(data=self.indent_transaction_data)
        
    #     self.assertTrue(serializer.is_valid())
        
    #     serializer.save()

    #     indent_transaction = IndentInventoryTransaction.objects.get(inventory_transaction_id='INDENT1')
    #     # print('indent_transaction_from_db',indent_transaction)
    #     self.assertEqual(indent_transaction.inventory_transaction_type, 'indent')
    #     self.assertEqual(indent_transaction.status, 'pending')
    #     self.assertEqual(indent_transaction.supplier, self.supplier)
    #     self.assertEqual(indent_transaction.supplyOrderNo, 'SO1')

    #     transaction_items = InventoryTransactionItem.objects.filter(inventory_transaction=indent_transaction)
    #     self.assertEqual(transaction_items.count(), 2)
        
    #     # print('-------End of test_create_indent_inventory_transaction-------\n ')

    def test_retrieve_indent_inventory_transaction(self):
        # --To clear terminal
        os.system('clear')
        print('\n-------test_retrieve_indent_inventory_transaction------- ')
        IndentInventoryTransaction.objects.all().delete()
        print('------data input to serializer------')
        print(self.indent_transaction_data)
        print('------------------------------------')
        serializer = IndentInventoryTransactionSerializer(data=self.indent_transaction_data)
        if(serializer.is_valid()):
            serializer.save()
        else:
            print('serializer is not valid')
            print(serializer.errors)    

        indent_transaction = IndentInventoryTransaction.objects.get(inventory_transaction_id='INDENT1')
        serializer = IndentInventoryTransactionSerializer(indent_transaction)
        print('\n-------serializer data------- ')
        print(serializer.data)

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
    #         } for item in InventoryTransactionItem.objects.filter(inventory_transaction=indent_transaction)
    #     ]

    #     self.assertEqual(serializer.data, expected_data)