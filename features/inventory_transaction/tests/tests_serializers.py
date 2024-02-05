# from datetime import date
# import json
# import os
# from features.base.base_test_setup_class import BaseTestCase
# from features.id_manager.models import IdManager
# from features.item.models import Item


# from features.supplier.models import Supplier
# from .models import  InventoryTransaction, InventoryTransactionItem, IndentInventoryTransaction, ItemBatch
# from .serializers import IndentInventoryTransactionSerializer

# class IndentInventoryTransactionSerializerTestCase(BaseTestCase):
#     def setUp(self):
#         super().setUp()
#         self.item = Item.objects.create(
#             name="Test Item",
#             description="Test Description",
#             type=self.item_type,
#             unit_of_measurement=self.unit_of_measurement,
#             is_active=True
#         )
#         self.item.save()

#         self.supplier = Supplier.objects.create(
#             name='Test Supplier',
#             contact_no=1234567890,
#             email='test@gmail.com',
#             address='Test Address',
#             is_active=True
       
#         )
#         self.supplier.save()
#         self.item_batch1=ItemBatch.objects.create(
#             batch_id='B2',
#             description='Test Batch 1',
#             date_of_expiry=date.today(),
#             item=self.item
#         )
#         self.item_batch1.save()

        
#         self.indent_transaction_data = {
#             'inventory_transaction_type': InventoryTransaction.TransactionTypes.INDENT,
#             'supplier': self.supplier.id,
#             'supply_order_no': 'SO1',
#             'supply_order_date': '2022-01-01',
#             'date_of_delivery': '2022-01-01',
#             'remarks': None,
#             'inventory_transaction_item_set': [
#                 {
#                     'item_batch': self.item_batch1.id,
#                     'quantity': 10,
#                     'is_active': True
#                 },
#                 {
#                     'item_batch': self.item_batch1.id,
#                     'quantity': 5,
#                     'is_active': True
#                 }
#             ]
#         }
#         # print('\n---------------\n')
#         # print(self.indent_transaction_data)
#         # print('\n---------------\n')

#     def test_create_indent_inventory_transaction(self):
#         # print('\n-------test_create_indent_inventory_transaction------- ')
#         IndentInventoryTransaction.objects.all().delete()
#         # print('------data input to serializer------')
#         # print(self.indent_transaction_data)
#         # print('\n\n')
#         IndentInventoryTransaction.objects.all().delete()
#         serializer = IndentInventoryTransactionSerializer(data=self.indent_transaction_data)
        
#         self.assertTrue(serializer.is_valid())
        
#         serializer.save()
#         # indent_transaction = IndentInventoryTransaction.objects.get(inventory_transaction_id='INDENT1')
        
#         indent_transaction = IndentInventoryTransaction.objects.all().first() 
#         # print('indent_transaction_from_db',indent_transaction)
#         self.assertEqual(indent_transaction.inventory_transaction_type, InventoryTransaction.TransactionTypes.INDENT)
#         self.assertEqual(indent_transaction.supplier, self.supplier)
#         self.assertEqual(indent_transaction.supply_order_no, 'SO1')

#         transaction_items = InventoryTransactionItem.objects.filter(inventory_transaction=indent_transaction)
#         self.assertEqual(transaction_items.count(), 2)
        
#         # print('-------End of test_create_indent_inventory_transaction-------\n ')

#     def test_retrieve_indent_inventory_transaction(self):
#         # --To clear terminal
#         # os.system('clear')
#         # print('\n-------test_retrieve_indent_inventory_transaction------- ')
#         self.maxDiff = None
#         IndentInventoryTransaction.objects.all().delete()
#         InventoryTransaction.objects.all().delete()
#         # print('------data input to serializer------')
#         # print(self.indent_transaction_data)
#         # print('------------------------------------')
#         serializer = IndentInventoryTransactionSerializer(data=self.indent_transaction_data)
#         if(serializer.is_valid()):
#             serializer.save()
#         else:
#             print('serializer is not valid')
#             print(serializer.errors)    

#         indent_transaction = IndentInventoryTransaction.objects.all().first()
#         serializer = IndentInventoryTransactionSerializer(indent_transaction)
#         # print('\n-------serializer data------- ')
#         # print(serializer.data)

#         expected_data = self.indent_transaction_data.copy()
#         expected_data['id'] = indent_transaction.id
#         expected_data['supplier'] = {
#             'id': self.supplier.id,
#             'name': 'Test Supplier',
#             'contact_no': 1234567890,
#             'email': 'test@gmail.com',
#             'address': 'Test Address',
#             'remarks': None,
#             'is_active': True
#         }
#         expected_data['date_time'] = indent_transaction.date_time.strftime('%d-%m-%Y %H:%M')
#         expected_data['inventory_transaction_item_set'] = [
#             {
#                 'id': item.id,
#                 'inventory_transaction': indent_transaction.id,
#                 'item_batch': item.item_batch.id,
#                 'quantity': item.quantity,
#                 'is_active': item.is_active,
#             } for item in InventoryTransactionItem.objects.filter(inventory_transaction=indent_transaction)
#         ]
#         expected_data['inventory_transaction_type']='indent'

#         serializer_data = json.loads(json.dumps(serializer.data))
#         # print('\nserializer_data, ',serializer_data)
#         del serializer_data['inventory_transaction_id']
#         # Remove 'created_on' and 'updated_on' from serializer_data
#         serializer_data.pop('created_on', None)
#         serializer_data.pop('updated_on', None)
#         # datas=InventoryTransaction.objects.all()
#         # print('\n\n\nInventory Transaction data')
#         # for data in datas:
#         #     print(data.inventory_transaction_type)
#         # print('\n\nexpected data, ',expected_data)
#         # print('\n\nserializer data, ',serializer_data)
        
#         self.assertEqual(serializer_data, expected_data)