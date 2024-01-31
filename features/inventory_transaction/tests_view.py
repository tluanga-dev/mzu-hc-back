# from datetime import date
# from django.urls import reverse

# from features.base.base_test_setup_class import BaseTestCase
# from features.item.item.models import Item
# from features.item.item_batch.models import ItemBatch
# from features.supplier.models import Supplier
# from .models import IndentInventoryTransaction, InventoryTransactionItem
# from .serializers import IndentInventoryTransactionSerializer
# from rest_framework.test import APIClient,APITestCase
# from rest_framework import status
# class IndentInventoryTransactionViewSetTest(BaseTestCase):
#     def setUp(self):
#         super().setUp()
#         self.client = APIClient()
#         # Add setup data here. For example, create some Supplier and InventoryTransactionItem instances
#         Item.objects.all().delete()
        
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
#             contact_no='1234567890',
#             email='test@gmail.com'
#         )
#         self.item_batch = ItemBatch.objects.create(
#             batch_id='B2',
#             description='Test Batch 1',
#             date_of_expiry=date.today(),
#             item=self.item
#         )
        
#     def tearDown(self):
#         # Clean up database after each test
#         InventoryTransactionItem.objects.all().delete()
#         IndentInventoryTransaction.objects.all().delete()
#         super().tearDown()

#     def test_create_indentinventorytransaction(self):
#         url = reverse('indent-inventory-transactions-list')  # Replace with the actual name of the URL
#         data = {
#             'supplier': self.supplier.id,
#             'supplyOrderNo': 'SO1',
#             'supplyOrderDate': '2022-01-01',
#             'dateOfDeliverty': '2022-01-01',
#             'inventorytransactionitem_set': [
#                 {'item_batch': self.item_batch.id, 'quantity': 10, 'is_active': True},
#             ],
#             'inventory_transaction_type': 'indent',
#             'inventory_transaction_id': 'INDENT1',
#             'remarks': None,
#             'date_time': '2024-01-27 22:08:00',
#             'status': 'pending',
#         }
#         response = self.client.post(url, data, format='json')
#         print('-------response data-------')
#         print(response.data)
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(IndentInventoryTransaction.objects.count(), 1)
#         created_instance = IndentInventoryTransaction.objects.first()
#         self.assertEqual(created_instance.supplier.id, data['supplier'])
#         # Add more assertions to check other fields of the created instance
