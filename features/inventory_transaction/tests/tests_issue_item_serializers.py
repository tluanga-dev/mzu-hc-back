from datetime import date
import json
import os
from features.base.base_test_setup_class import BaseTestCase
from features.id_manager.models import IdManager
from features.inventory_transaction.models import InventoryTransaction, InventoryTransactionItem, IssueItemInventoryTransaction
from features.inventory_transaction.serializers import IssueItemInventoryTransactionSerializer
from features.item.models import Item, ItemBatch


from features.supplier.models import Supplier


class IsssueItemInventoryTransactionSerializerTestCase(BaseTestCase):
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
        self.item_batch1=ItemBatch.objects.create(
            batch_id='B2',
            description='Test Batch 1',
            date_of_expiry=date.today(),
            item=self.item
        )
        self.item_batch1.save()

        
        self.issue_item_transaction_data = {
            'issue_to': 'Test Issue To',
            'issue_date': '2022-01-01',
            'remarks': None,
            'inventory_transaction_item_set': [
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

    def test_create_issue_item_inventory_transaction(self):
        # print('\n-------test_create_indent_inventory_transaction------- ')
        IssueItemInventoryTransaction.objects.all().delete()
        InventoryTransactionItem.objects.all().delete()
        serializer = IssueItemInventoryTransactionSerializer(data=self.issue_item_transaction_data)
       
        if(serializer.is_valid()):
            # print('serializer is valid')
            serializer.save()
        else:
            print('serializer is not valid')
            print(serializer.errors)    
        self.assertTrue(serializer.is_valid())
        
    
        issue_transaction = IssueItemInventoryTransaction.objects.all().first()
       
        self.assertEqual(issue_transaction.inventory_transaction_type, issue_transaction.TransactionTypes.ITEM_ISSUE)
       
        self.assertEqual(issue_transaction.issue_to, 'Test Issue To')

        transaction_items = InventoryTransactionItem.objects.filter(inventory_transaction=issue_transaction)
        
        self.assertEqual(transaction_items.count(), 2)
        
        

    def test_retrieve_issue_item_inventory_transaction(self):
        # --To clear terminal
        # os.system('clear')
        # print('\n-------test_retrieve_indent_inventory_transaction------- ')
        self.maxDiff = None
        IssueItemInventoryTransaction.objects.all().delete()
        InventoryTransactionItem.objects.all().delete()
        InventoryTransaction.objects.all().delete() 
        
        # print('------data input to serializer------')
        # print(self.indent_transaction_data)
        # print('------------------------------------')
        serializer = IssueItemInventoryTransactionSerializer(data=self.issue_item_transaction_data)
        if(serializer.is_valid()):
            print('serializer is  valid')
            serializer.save()
        else:
            print('serializer is not valid')
            print(serializer.errors)   
        issue_item_transaction = None 

        issue_item_transaction =  IssueItemInventoryTransaction.objects.first()
        serializer = IssueItemInventoryTransactionSerializer(issue_item_transaction)
       

        expected_data = self.issue_item_transaction_data.copy()
        expected_data['id'] = issue_item_transaction.id
        
        expected_data['date_time'] = issue_item_transaction.date_time.strftime('%d-%m-%Y %H:%M')
        expected_data['inventory_transaction_item_set'] = [
            {
                'id': item.id,
                'inventory_transaction': issue_item_transaction.id,
                'item_batch': item.item_batch.id,
                'quantity': item.quantity,
                'is_active': item.is_active,
            } for item in InventoryTransactionItem.objects.filter(inventory_transaction=issue_item_transaction)
        ]
        expected_data['inventory_transaction_type']=InventoryTransaction.TransactionTypes.ITEM_ISSUE

        serializer_data = json.loads(json.dumps(serializer.data))
        # print('\nserializer_data, ',serializer_data)
        del serializer_data['inventory_transaction_id']
        # Remove 'created_on' and 'updated_on' from serializer_data
        serializer_data.pop('created_on', None)
        serializer_data.pop('updated_on', None)
        # datas=InventoryTransaction.objects.all()
        # print('\n\n\nInventory Transaction data')
        # for data in datas:
        #     print(data.inventory_transaction_type)
        # print('\n\nexpected data, ',expected_data)
        # print('\n\nserializer data, ',serializer_data)
        
        self.assertEqual(serializer_data, expected_data)