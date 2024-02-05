from datetime import date
import os
from django.urls import reverse

from features.base.base_test_setup_class import BaseTestCase
from features.item.models import Item, ItemBatch

from features.supplier.models import Supplier
from .models import IndentInventoryTransaction, InventoryTransactionItem
from .serializers import IndentInventoryTransactionSerializer
from rest_framework.test import APIClient,APITestCase
from rest_framework import status
class IndentInventoryTransactionViewSetTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.client = APIClient()
        # Add setup data here. For example, create some Supplier and InventoryTransactionItem instances
        Item.objects.all().delete()
        InventoryTransactionItem.objects.all().delete()
        IndentInventoryTransaction.objects.all().delete()
        self.item = Item.objects.create(
            name="Test Item",
            description="Test Description",
            type=self.item_type,
            unit_of_measurement=self.unit_of_measurement,
            is_active=True
        )
        self.supplier = Supplier.objects.create(
            name='Test Supplier', 
            address='Test Address', 
            contact_no=1234567890,
            email='test@gmail.com'
        )
        self.item_batch = ItemBatch.objects.create(
            batch_id='B2',
            description='Test Batch 1',
            date_of_expiry=date.today(),
            item=self.item
        )
        
    def tearDown(self):
        # Clean up database after each test
        InventoryTransactionItem.objects.all().delete()
        IndentInventoryTransaction.objects.all().delete()
        super().tearDown()

    def test_create_indentinventorytransaction(self):
     
        # print('\n\ntest_create_indentinventorytransaction\n\n')
        url = reverse('indent-inventory-transactions-list')  # Replace with the actual name of the URL
        data = {
            'supplier': self.supplier.id,
            'supplyOrderNo': 'SO1',
            'supplyOrderDate': '2022-01-01',
            'dateOfDeliverty': '2022-01-01',
            'inventorytransactionitem_set': [
                {'item_batch': self.item_batch.id, 'quantity': 10, 'is_active': True},
            ],
            'inventory_transaction_type': 'indent',
            'inventory_transaction_id': 'INDENT1',
            'remarks': None,
            'date_time': '2024-01-27 22:08:00',
            'status': 'pending',
        }
        response = self.client.post(url, data, format='json')
        # print('-------response data-------')
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(IndentInventoryTransaction.objects.count(), 1)
        created_instance = IndentInventoryTransaction.objects.first()
        self.assertEqual(created_instance.supplier.id, data['supplier'])
        # Add more assertions to check other fields of the created instance
    
    def test_get_indent_transactions(self):
     

        url = reverse('indent-inventory-transactions-list')
        data = {
            'supplier': self.supplier.id,
            'supplyOrderNo': 'SO1',
            'supplyOrderDate': '2022-01-01',
            'dateOfDeliverty': '2022-01-01',
            'inventorytransactionitem_set': [
                {'item_batch': self.item_batch.id, 'quantity': 10, 'is_active': True},
            ],
            'inventory_transaction_type': 'indent',
            'inventory_transaction_id': 'INDENT1',
            'remarks': None,
            'date_time': '2024-01-27 22:08:00',
            'status': 'pending',
        }
        response = self.client.post(url, data, format='json')

        data_2 = {
            'supplier': self.supplier.id,
            'supplyOrderNo': 'SO12',
            'supplyOrderDate': '2022-01-01',
            'dateOfDeliverty': '2022-01-01',
            'inventorytransactionitem_set': [
                {'item_batch': self.item_batch.id, 'quantity': 10, 'is_active': True},
            ],
            'inventory_transaction_type': 'indent',
            'inventory_transaction_id': 'INDENT2',
            'remarks': None,
            'date_time': '2024-01-27 22:08:00',
            'status': 'pending',
        }
        response = self.client.post(url, data_2, format='json')
        print('\n\ntest_get_indent_transactions\n\n')
        
        response = self.client.get(url)
        print('-------response data-------')
        print(response.data)
        print(len(response.data))


    def test_get_indent_transactions(self):
      
        url = reverse('indent-inventory-transactions-list')
        indent_transaction = IndentInventoryTransaction.objects.create(
        supplier=self.supplier,
        supplyOrderNo='SO1',
        supplyOrderDate='2022-01-01',
        dateOfDeliverty='2022-01-01',
        inventory_transaction_type='indent',
        inventory_transaction_id='INDENT1',
        date_time='2024-01-27 22:08:00',
      
            )
        url = reverse('indent-inventory-transactions-detail', kwargs={'pk': indent_transaction.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], indent_transaction.pk)

    def test_filter_indentinventorytransaction(self):
        
        
       
        url = reverse('indent-inventory-transactions-list')
        IndentInventoryTransaction.objects.all().delete()
        InventoryTransactionItem.objects.all().delete()
        data = {
            'id':1,
            'supplier': self.supplier.id,
            'supplyOrderNo': 'SO1',
            'supplyOrderDate': '2022-01-01',
            'dateOfDeliverty': '2022-01-01',
            'inventorytransactionitem_set': [
                {'item_batch': self.item_batch.id, 'quantity': 10, 'is_active': True},
            ],
            'inventory_transaction_type': 'indent',
            'inventory_transaction_id': 'INDENT1',
            'remarks': None,
            'date_time': '2024-01-27 22:08:00',
            'status': 'pending',
        }
        response = self.client.post(url, data, format='json')

        data_2 = {
            'id': 200,
            'supplier': self.supplier.id,
            'supplyOrderNo': 'SO12',
            'supplyOrderDate': '2022-01-01',
            'dateOfDeliverty': '2022-01-01',
            'inventorytransactionitem_set': [
                {'item_batch': self.item_batch.id, 'quantity': 10, 'is_active': True},
            ],
            'inventory_transaction_type': 'indent',
            'inventory_transaction_id': 'INDENT2',
            'remarks': 'This is supply order 2',
            'date_time': '2024-01-27 22:08:00',
            'status': 'pending',
        }
        response = self.client.post(url, data_2, format='json')

        response = self.client.get(url)
        id=response.data[1]['id']
        url = reverse('indent-inventory-transactions-detail', kwargs={'pk': id})
        response = self.client.get(url)
        # print('-------response data without filter-------')
        # print(response.data)
        # print('\n\n')
        # print('-------response data with filter-------')
        
        url = reverse('indent-inventory-transactions-list') + '?supplyOrderNo=SO12'
        response2 = self.client.get(url)
       
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response2.data), 1)  # Check that one instance is returned
        # self.assertEqual(response.data[0]['supplyOrderNo'], 'SO12')  # Check that the returned instance has the correct supplyOrderNo


    def test_filter_indentinventorytransaction_by_date(self):
        
        url = reverse('indent-inventory-transactions-list')
        data = {
            'id':1,
            'supplier': self.supplier.id,
            'supplyOrderNo': 'SO1',
            'supplyOrderDate': '2022-01-01',
            'dateOfDeliverty': '2022-01-01',
            'inventorytransactionitem_set': [
                {'item_batch': self.item_batch.id, 'quantity': 10, 'is_active': True},
            ],
            'inventory_transaction_type': 'indent',
            'inventory_transaction_id': 'INDENT1',
            'remarks': None,
            'date_time': '2024-01-27 22:08:00',
            'status': 'pending',
        }
        response = self.client.post(url, data, format='json')

        data_2 = {
            'id': 200,
            'supplier': self.supplier.id,
            'supplyOrderNo': 'SO12',
            'supplyOrderDate': '2022-03-01',
            'dateOfDeliverty': '2022-01-01',
            'inventorytransactionitem_set': [
                {'item_batch': self.item_batch.id, 'quantity': 10, 'is_active': True},
            ],
            'inventory_transaction_type': 'indent',
            'inventory_transaction_id': 'INDENT2',
            'remarks': 'This is supply order 2',
            'date_time': '2024-01-27 22:08:00',
            'status': 'pending',
        }
        response = self.client.post(url, data_2, format='json')

        # Test filtering by an exact date
        response = self.client.get(reverse('indent-inventory-transactions-list'), {'supplyOrderDate': '2022-01-01'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data),1)
        self.assertEqual(response.data[0]['supplyOrderDate'], '2022-01-01')

        # Test filtering by a range of dates
        response = self.client.get(reverse('indent-inventory-transactions-list'), {'supplyOrderDateFrom': '2022-02-01', 'supplyOrderDateTo': '2022-04-01'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

         # Test filtering by a range of dates
        response = self.client.get(reverse('indent-inventory-transactions-list'), {'supplyOrderDateFrom': '2022-01-01', 'supplyOrderDateTo': '2022-04-01'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)