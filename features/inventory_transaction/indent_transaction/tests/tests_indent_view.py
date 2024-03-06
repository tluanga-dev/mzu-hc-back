# from datetime import date
# import os
# from django.urls import reverse

# from features.base.base_test_setup_class import BaseTestCase
# from features.inventory_transaction.indent_transaction.models import IndentInventoryTransaction
# from features.inventory_transaction.inventory_transaction.models import InventoryTransactionItem
# from features.item.models import Item, ItemBatch

# from features.supplier.models import Supplier
# from rest_framework.test import APIClient,APITestCase
# from rest_framework import status

# from features.utils.print_json import print_json_string
# class IndentInventoryTransactionViewSetTest(BaseTestCase):
#     def setUp(self):
#         super().setUp()
#         self.client = APIClient()
#         # Add setup data here. For example, create some Supplier and InventoryTransactionItem instances
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
#         self.item_batch_1 = ItemBatch.objects.create(
#             batch_id='B1',
#             description='Test Batch 1',
#             date_of_expiry=date.today(),
#             item=self.item
#         )

#         self.item_batch_2 = ItemBatch.objects.create(
#             batch_id='B2',
#             description='Test Batch 2',
#             date_of_expiry=date.today(),
#             item=self.item
#         )
       

#     def tearDown(self):
#         # Clean up database after each test
#         InventoryTransactionItem.objects.all().delete()
#         IndentInventoryTransaction.objects.all().delete()
#         super().tearDown()

#     def test_create_indentinventorytransaction(self):
     
#         # ('\n\ntest_create_indentinventorytransaction\n\n')
#         url = reverse('indent-inventory-transactions-list')  # Replace with the actual name of the URL
#         data = {
#             'supplier': str(self.supplier.id),
#             'supply_order_no': 'SO1',
#             'supply_order_date': '01-01-2023',
#             'date_of_delivery': '03-02-2023',
#             'inventory_transaction_item_set': [
#                 {
#                     'item_batch': str(self.item_batch_1.id), 
#                     'quantity': 10, 
#                     'is_active': True
#                 },
#             ],
#             'inventory_transaction_type': 'indent',
#             'remarks': None,
#             'status': 'pending',
#         }
#         response = self.client.post(url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(IndentInventoryTransaction.objects.count(), 1)
#         created_instance = IndentInventoryTransaction.objects.first()
#         self.assertEqual(str(created_instance.supplier.id), data['supplier'])
      
    
#     def test_get_indent_transactions(self):
        
#         url = reverse('indent-inventory-transactions-list')
#         data = {
#             'supplier': str(self.supplier.id),
#             'supply_order_no': 'SO1',
#             'supply_order_date': '03-03-2024',
#             'date_of_delivery': '03-04-2024',
#             'inventory_transaction_item_set': [
#                 {'item_batch': str(self.item_batch_1.id), 'quantity': 10, 'is_active': True},
#             ],
#             'inventory_transaction_type': 'indent',
#             'remarks': None,
      
#             'status': 'pending',
#         }
#         response = self.client.post(url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         response=self.client.get(url)
        

#         data_2 = {
#             'supplier': str(self.supplier.id),
#              'supply_order_no': 'SO2',
#             'supply_order_date': '03-01-2024',
#             'date_of_delivery': '23-03-2024',
#             'inventory_transaction_item_set': [
#                 {'item_batch': str(self.item_batch_2.id), 'quantity': 10, 'is_active': True},
#             ],
#             'inventory_transaction_type': 'indent',
#             'inventory_transaction_id': 'INDENT2',
#             'remarks': None,
#             'status': 'pending',
#         }
#         response = self.client.post(url, data_2, format='json')
        
#         if(response.status_code!=201):
#             (response.content)
#         self.assertEquals(response.status_code, status.HTTP_201_CREATED)

#         url = reverse('indent-inventory-transactions-list')
#         response=self.client.get(url)
#         print_json_string(response.data)

        


#     # def test_get_indent_transactions(self):
      
#     #     url = reverse('indent-inventory-transactions-list')
#     #     indent_transaction = IndentInventoryTransaction.objects.create(
#     #     supplier=self.supplier,
#     #     supply_order_no='SO1',
#     #     supply_order_date='2022-01-01',
#     #     date_of_delivery='2022-01-01',
#     #     inventory_transaction_type='indent',
#     #     inventory_transaction_id='INDENT1',
#     #     )
#     #     url = reverse('indent-inventory-transactions-detail', kwargs={'pk': indent_transaction.pk})
 
#     #     response = self.client.get(url)
      
        
#     #     self.assertEqual(response.status_code, status.HTTP_200_OK)
#     #     self.assertEqual(response.data['id'], str(indent_transaction.pk))


    
#     # def test_filter_indent_inventory_transaction(self):
#     #     url = reverse('indent-inventory-transactions-list')
#     #     IndentInventoryTransaction.objects.all().delete()
#     #     InventoryTransactionItem.objects.all().delete()
#     #     data = {
#     #         'supplier': self.supplier.id,
#     #         'supply_order_no': 'SO1',
#     #         'supply_order_date': '01-01-2023',
#     #         'date_of_delivery': '01-04-2023',
#     #         'inventory_transaction_item_set': [
#     #             {
#     #                 'item_batch': self.item_batch_1.id, 
#     #                 'quantity': 10, 
#     #                 'is_active': True,
#     #                 'inventory_transaction_type': 'indent',
#     #                 },
#     #         ],
#     #         'inventory_transaction_type': 'indent',
#     #         'inventory_transaction_id': 'INDENT1',
#     #         'remarks': None,
#     #         'status': 'pending',
#     #     }
#     #     response = self.client.post(url, data, format='json')
#     #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)

#     #     data_2 = {
#     #         'supplier': self.supplier.id,
#     #         'supply_order_no': 'SO12',
#     #         'supply_order_date': '01-01-2023',
#     #         'date_of_delivery': '03-01-2023',
#     #         'inventory_transaction_item_set': [
#     #             {
#     #                 'item_batch': self.item_batch_2.id,
#     #                   'quantity': 10,
#     #                     'is_active': True,
#     #                     'inventory_transaction_type': 'indent',
#     #             },
#     #         ],
#     #         'inventory_transaction_type': 'indent',
#     #         'inventory_transaction_id': 'INDENT2',
#     #         'remarks': 'This is supply order 2',
#     #         'status': 'pending',
#     #     }
      
#     #     response_2 = self.client.post(url, data_2, format='json')
        
        
        
#     #     response = self.client.get(url)

#     #     (response.data)

#     #     id=response.data[1]['id']
#     #     url = reverse('indent-inventory-transactions-detail', kwargs={'pk': id})
#     #     response = self.client.get(url)
        
        
#     #     url = reverse('indent-inventory-transactions-list') + '?supply_order_no=SO12'
#     #     filtered_response = self.client.get(url)
#     #     ('\nfiltered_response\n')
#     #     (filtered_response.data)
       
#     #     self.assertEqual(filtered_response.status_code, status.HTTP_200_OK)
        
#     #     self.assertEqual(len(filtered_response.data), 1)  # Check that one instance is returned
#     #     self.assertEqual(filtered_response.data[0]['supply_order_no'], 'SO12')  # Check that the returned instance has the correct supplyOrderNo

       
#     # def test_filter_indentinventorytransaction_by_date(self):
        
#     #     url = reverse('indent-inventory-transactions-list')
#     #     data = {
#     #         'id':1,
#     #         'supplier': self.supplier.id,
#     #         'supply_order_no': 'SO1',
#     #         'supply_order_date': '01-01-2022',
#     #         'date_of_delivery': '01-01-2022',
#     #         'inventory_transaction_item_set': [
#     #             {'item_batch': self.item_batch_1.id, 'quantity': 40, 'is_active': True},
#     #         ],
#     #         'inventory_transaction_type': 'indent',
#     #         'inventory_transaction_id': 'INDENT1',
#     #         'remarks': None,
            
#     #         'status': 'pending',
#     #     }
#     #     response = self.client.post(url, data, format='json')
#     #     (response)

#     #     data_2 = {
#     #         'id': 200,
#     #         'supplier': self.supplier.id,
#     #         'supply_order_no': 'SO12',
#     #         'supply_order_date': '01-03-2023',
#     #         'date_of_delivery': '01-04-2023',
#     #         'inventory_transaction_item_set': [
#     #             {'item_batch': self.item_batch_2.id, 'quantity': 10, 'is_active': True},
#     #         ],
#     #         'inventory_transaction_type': 'indent',
#     #         'inventory_transaction_id': 'INDENT2',
#     #         'remarks': 'This is supply order 2',
          
#     #         'status': 'pending',
#     #     }
#     #     response = self.client.post(url, data_2, format='json')
       

#     #     # # Test filtering by an exact date
#     #     response = self.client.get(reverse('indent-inventory-transactions-list'), {'supply_order_date': '01-01-2022'})
        
#     #     self.assertEqual(response.status_code, status.HTTP_200_OK)
#     #     self.assertEqual(len(response.data),1)
#     #     self.assertEqual(response.data[0]['supply_order_date'], '01-01-2022')

#     #     # Test filtering by a range of dates
#     #     response = self.client.get(reverse('indent-inventory-transactions-list'), {'supply_order_dateFrom': '01-02-2022', 'supply_order_dateTo': '01-03-2024'})
#     #     self.assertEqual(response.status_code, status.HTTP_200_OK)
#     #     self.assertEqual(len(response.data), 1)

#     #      # Test filtering by a range of dates
#     #     response = self.client.get(reverse('indent-inventory-transactions-list'), {'supply_order_dateFrom': '01-01-2022', 'supply_order_dateTo': '01-04-2024'})
#     #     self.assertEqual(response.status_code, status.HTTP_200_OK)
#     #     self.assertEqual(len(response.data), 2)