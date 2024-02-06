# from datetime import date
# import os
# from django.urls import reverse
# from features import id_manager

# from features.base.base_test_setup_class import BaseTestCase
# from features.id_manager.models import IdManager
# from features.inventory_transaction.models import IndentInventoryTransaction, InventoryTransactionItem, IssueItemInventoryTransaction
# from features.item.models import Item, ItemBatch

# from features.supplier.models import Supplier
# from rest_framework.test import APIClient,APITestCase
# from rest_framework import status
# class IssueITemInventoryTransactionViewSetTest(BaseTestCase):
#     def setUp(self):
#         super().setUp()
#         Item.objects.all().delete()
#         InventoryTransactionItem.objects.all().delete()
#         IndentInventoryTransaction.objects.all().delete()
#         self.item = Item.objects.create(
#             name="Test Item",
#             description="Test Description",
#             type=self.item_type,
#             unit_of_measurement=self.unit_of_measurement,
#             is_active=True
#         )
#         self.supplier = Supplier.objects.create(
#             name='Test Supplier', 
#             address='Test Address', 
#             contact_no=1234567890,
#             email='test@gmail.com'
#         )
#         self.item_batch = ItemBatch.objects.create(
#             batch_id='B2',
#             description='Test Batch 1',
#             date_of_expiry=date.today(),
#             item=self.item
#         )
#         self.issue_item_transaction_data = {
#             'issue_to': 'Test Issue To',
#             'issue_date': '2022-01-01',
#             'remarks': None,
#             'inventory_transaction_item_set': [
#                 {
#                     'item_batch': self.item_batch.id,
#                     'quantity': 10,
#                     'is_active': True
#                 },
#                 {
#                     'item_batch': self.item_batch.id,
#                     'quantity': 5,
#                     'is_active': True
#                 }
#             ]
#         }

#         self.issue_item_transaction_data_2 = {
#             'issue_to': 'Test Issue To 2',
#             'issue_date': '2022-05-01',
#             'remarks': None,
#             'inventory_transaction_item_set': [
#                 {
#                     'item_batch': self.item_batch.id,
#                     'quantity': 10,
#                     'is_active': True
#                 },
#                 {
#                     'item_batch': self.item_batch.id,
#                     'quantity': 5,
#                     'is_active': True
#                 }
#             ]
#         }
        
#     def tearDown(self):
#         # Clean up database after each test
#         InventoryTransactionItem.objects.all().delete()
#         IssueItemInventoryTransaction.objects.all().delete()
#         IdManager.objects.all().delete()
#         super().tearDown()

#     def test_create_issue_item_inventorytransaction(self):
#         self.tearDown()
#         # print('\n\ntest_create_indentinventorytransaction\n\n')
#         url = reverse('issue-item-inventory-transactions-list')  # Replace with the actual name of the URL
        
#         response = self.client.post(url, self.issue_item_transaction_data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(IssueItemInventoryTransaction.objects.count(), 1)
#         created_instance = IssueItemInventoryTransaction.objects.first()
#         self.assertEqual(created_instance.issue_to, 'Test Issue To')  # Check that the created instance has the correct issueTo
#         # Add more assertions to check other fields of the created instance
    
#     def test_get_indent_transactions(self):
    
#         url = reverse('issue-item-inventory-transactions-list')
        
#         response = self.client.post(url, self.issue_item_transaction_data, format='json')
#         response = self.client.post(url, self.issue_item_transaction_data, format='json')

        
#         response = self.client.get(url)
#         print('-------response data-------')
#         print(response.data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 2)  # Check that two instances are returned
       


#     def test_get_indent_transactions(self):
#         self.tearDown()
#         url = reverse('issue-item-inventory-transactions-list')
#         response = self.client.post(url, self.issue_item_transaction_data, format='json')
       
#         id=response.data['id']
#         url = reverse('issue-item-inventory-transactions-detail', kwargs={'pk': id})
#         response = self.client.get(url)
        
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['id'], id)  # Check that the returned instance has the correct id


    
#     def test_filter_indent_inventory_transaction(self):
#         self.tearDown()
#         url = reverse('issue-item-inventory-transactions-list')
        
#         self.client.post(url, self.issue_item_transaction_data_2, format='json')
#         response = self.client.post(url, self.issue_item_transaction_data, format='json')
       
#         response = self.client.get(url)
  

#         id=response.data[1]['id']
#         url = reverse('indent-inventory-transactions-detail', kwargs={'pk': id})
#         response = self.client.get(url)
#         # print('-------response data without filter-------')
#         # print(response.data)
#         # print('\n\n')
#         # print('-------response data with filter-------')
        
#         url = reverse('indent-inventory-transactions-list') + '?issue_to=Test-Issue To'
#         filtered_response = self.client.get(url)
#         print(filtered_response.data)
#         print(url)
       
#         # self.assertEqual(filtered_response.status_code, status.HTTP_200_OK)
#         # self.assertEqual(len(filtered_response.data), 1)  # Check that one instance is returned
#         # self.assertEqual(filtered_response.data[0]['supply_order_no'], 'SO12')  # Check that the returned instance has the correct supplyOrderNo


#     # def test_filter_indentinventorytransaction_by_date(self):
        
#     #     url = reverse('indent-inventory-transactions-list')
#     #     data = {
#     #         'id':1,
#     #         'supplier': self.supplier.id,
#     #         'supply_order_no': 'SO1',
#     #         'supply_order_date': '2022-01-01',
#     #         'date_of_delivery': '2022-01-01',
#     #         'inventory_transaction_item_set': [
#     #             {'item_batch': self.item_batch.id, 'quantity': 10, 'is_active': True},
#     #         ],
#     #         'inventory_transaction_type': 'indent',
#     #         'inventory_transaction_id': 'INDENT1',
#     #         'remarks': None,
#     #         'date_time': '2024-01-27 22:08:00',
#     #         'status': 'pending',
#     #     }
#     #     response = self.client.post(url, data, format='json')
  

#     #     data_2 = {
#     #         'id': 200,
#     #         'supplier': self.supplier.id,
#     #         'supply_order_no': 'SO12',
#     #         'supply_order_date': '2022-03-01',
#     #         'date_of_delivery': '2022-01-01',
#     #         'inventory_transaction_item_set': [
#     #             {'item_batch': self.item_batch.id, 'quantity': 10, 'is_active': True},
#     #         ],
#     #         'inventory_transaction_type': 'indent',
#     #         'inventory_transaction_id': 'INDENT2',
#     #         'remarks': 'This is supply order 2',
#     #         'date_time': '2024-01-27 22:08:00',
#     #         'status': 'pending',
#     #     }
#     #     response = self.client.post(url, data_2, format='json')

#     #     # Test filtering by an exact date
#     #     response = self.client.get(reverse('indent-inventory-transactions-list'), {'supply_order_date': '2022-01-01'})
#     #     # print(response.data)
#     #     self.assertEqual(response.status_code, status.HTTP_200_OK)
#     #     self.assertEqual(len(response.data),1)
#     #     self.assertEqual(response.data[0]['supply_order_date'], '2022-01-01')

#     #     # Test filtering by a range of dates
#     #     response = self.client.get(reverse('indent-inventory-transactions-list'), {'supply_order_dateFrom': '2022-02-01', 'supply_order_dateTo': '2022-04-01'})
#     #     self.assertEqual(response.status_code, status.HTTP_200_OK)
#     #     self.assertEqual(len(response.data), 1)

#     #      # Test filtering by a range of dates
#     #     response = self.client.get(reverse('indent-inventory-transactions-list'), {'supply_order_dateFrom': '2022-01-01', 'supply_order_dateTo': '2022-04-01'})
#     #     self.assertEqual(response.status_code, status.HTTP_200_OK)
#     #     self.assertEqual(len(response.data), 2)