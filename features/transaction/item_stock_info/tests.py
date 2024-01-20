# from django.test import TestCase
# from .models import ItemStockInfo
# from .serializers import ItemStockInfoSerializer

# class ItemStockInfoTestCase(TestCase):
#     def setUp(self):
   
#         self.item_stock_info = ItemStockInfo.objects.create(quantity=10)  # Add necessary fields
#         ItemStockInfo.objects.create(quantity=10, updated_on="2022-01-01T00:00:00Z")

#     def test_item_stock_info(self):
#         item_stock_info = ItemStockInfo.objects.get(id=1)
#         self.assertEqual(item_stock_info.quantity, 10)

   

#     def test_item_stock_info_serializer(self):
#         item_stock_info = ItemStockInfo.objects.get(id=1)
#         serializer = ItemStockInfoSerializer(item_stock_info)
#         expected_data = {'id': 1, 'quantity': 10, 'item': None, 'updated_on': "2022-01-01T00:00:00Z"}
#         actual_data = serializer.data
#         self.assertEqual(actual_data['id'], expected_data['id'])
#         self.assertEqual(actual_data['quantity'], expected_data['quantity'])
#         self.assertEqual(actual_data['item'], expected_data['item'])