# from django.test import TestCase
# from rest_framework.test import APIClient
# from .models import IndentInventoryTransaction, InventoryTransactionItem
# from .serializers import IndentInventoryTransactionSerializer

# class IndentInventoryTransactionViewSetTest(TestCase):
#     def setUp(self):
#         self.client = APIClient()

#     def test_create(self):
#         # Prepare data
#         data = {
#             "supplyOrderNo": "123",
#             "supplyOrderDate": "2022-01-01",
#             "dateOfDeliverty": "2022-01-02",
#             "inventory_transaction_type": "type1",
#             "inventory_transaction_id": "id1",
#             "inventory_transaction_item": [
#                 {
#                     # Fill in the fields for your InventoryTransactionItem
#                 },
#                 # Add more items if needed
#             ],
#             "remarks": "remarks1",
#             "status": "status1"
#         }

#         # Send POST request
#         response = self.client.post('/api/indentinventorytransaction/', data, format='json')

#         # Check response status code
#         self.assertEqual(response.status_code, 201)

#         # Check if the data in the response is correct
#         serializer = IndentInventoryTransactionSerializer(IndentInventoryTransaction.objects.get(id=response.data['id']))
#         self.assertEqual(response.data, serializer.data)