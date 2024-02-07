from datetime import date
import json
import os
from features.base.base_test_setup_class import BaseTestCase
from features.id_manager.models import IdManager
from features.inventory_transaction.models import IndentInventoryTransaction, InventoryTransaction, InventoryTransactionItem, IssueItemInventoryTransaction
from features.inventory_transaction.serializers import IndentInventoryTransactionSerializer, IssueItemInventoryTransactionSerializer
from features.item.models import Item, ItemBatch, ItemStockInfo
from features.organisation_section.models import  OrganisationSection
from features.organisation_section.serializers import OrganisationSectionSerializer


from features.supplier.models import Supplier


class IsssueItemInventoryTransactionSerializerTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        OrganisationSection.objects.all().delete()
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
        self.organization_section=OrganisationSection.objects.create(
            name='Test Organisation Section',
            code='TOS',
            description='Test Organisation Section',
        )


        # --------------------INDENT TRANSACTION---------------------
        self.supplier = Supplier.objects.create(
            name='Test Supplier',
            contact_no=1234567890,
            email='test@gmail.com',
            address='Test Address',
            is_active=True
       
        )
        self.supplier.save()
        self.indent_transaction_data = {
                'inventory_transaction_type': InventoryTransaction.TransactionTypes.INDENT,
                'supplier': self.supplier.id,
                'supply_order_no': 'SO1',
                'supply_order_date': '2022-01-01',
                'date_of_delivery': '2022-01-01',
                'remarks': None,
                'inventory_transaction_item_set': [
                    {
                        'item_batch': self.item_batch1.id,
                        'quantity': 100,
                        'is_active': True
                    },
                    {
                        'item_batch': self.item_batch1.id,
                        'quantity': 100,
                        'is_active': True
                    }
                ]
            }
        IndentInventoryTransaction.objects.all().delete()
        serializer=IndentInventoryTransactionSerializer(data=self.indent_transaction_data)
        
        if(serializer.is_valid()):
            serializer.save()
        else:
            print('serializer is not valid')
            print(serializer.errors)
        
        self.issue_item_transaction_data = {
            'issue_to': self.organization_section.id,
            'issue_date': '2022-01-01',
            'item_receiver': 'Test Item Receiver',
            'remarks': None,
            'inventory_transaction_item_set': [
                {
                    'item_batch': self.item_batch1.id,
                    'quantity': 10,
                    'is_active': True
                },
                {
                    'item_batch': self.item_batch1.id,
                    'quantity': 10,
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
       
        self.assertEqual(issue_transaction.issue_to, self.organization_section)

        transaction_items = InventoryTransactionItem.objects.filter(inventory_transaction=issue_transaction)
        
        self.assertEqual(transaction_items.count(), 2)

        # -----check Itemstock info---
        quantity=ItemStockInfo.objects.get(item=self.item).quantity
       
        self.assertEqual(quantity,180 )
        
        

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
        expected_data['issue_to']=OrganisationSectionSerializer(self.organization_section).data 
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
       
        
        del serializer_data['inventory_transaction_id']
     
        serializer_data.pop('created_on', None)
        serializer_data.pop('updated_on', None)
        
        # print('\n\nexpected data, ',expected_data)
        # print('\n\nserializer data, ',serializer_data)
        
        self.assertEqual(serializer_data, expected_data)      