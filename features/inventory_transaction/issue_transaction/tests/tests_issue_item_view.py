from datetime import date
import os
from django.urls import reverse
from features import id_manager

from features.base.base_test_setup_class import BaseTestCase
from features.id_manager.models import IdManager
from features.inventory_transaction.indent_transaction.models import IndentInventoryTransaction
from features.inventory_transaction.indent_transaction.serializers import IndentInventoryTransactionSerializer
from features.inventory_transaction.inventory_transaction.models import InventoryTransaction, InventoryTransactionItem, ItemStockInfo
from features.inventory_transaction.issue_transaction.models import IssueItemInventoryTransaction

from features.item.models import Item, ItemBatch
from features.organisation_unit.models import OrganisationSection

from features.supplier.models import Supplier
from rest_framework.test import APIClient,APITestCase
from rest_framework import status
class IssueITemInventoryTransactionViewSetTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        IdManager.objects.all().delete()
        IndentInventoryTransaction.objects.all().delete()  
        InventoryTransactionItem.objects.all().delete()
        IssueItemInventoryTransaction.objects.all().delete()
        ItemStockInfo.objects.all().delete()
        Item.objects.all().delete()
        OrganisationSection.objects.all().delete()
        self.item = Item.objects.create(
            name="Test Item",
            description="Test Description",
            type=self.item_type,
            unit_of_measurement=self.unit_of_measurement,
            is_active=True
        )
        self.item.save()
        self.item_batch=ItemBatch.objects.create(
            batch_id='B2',
            description='Test Batch 1',
            date_of_expiry=date.today(),
            item=self.item
        )
        self.item_batch.save()
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
                        'item_batch': self.item_batch.id,
                        'quantity': 1000,
                        'inventory_transaction_type': 'ITEM_INDENT',
                        'is_active': True
                    },
                    
                ]
            }
        IndentInventoryTransaction.objects.all().delete()
        serializer=IndentInventoryTransactionSerializer(data=self.indent_transaction_data)
       
        
        if(serializer.is_valid()):
            serializer.save()
            # print(serializer.data)
        else:
            print('serializer is not valid')
            print(serializer.errors)
       
        # --------Data for Issue Item Inventory Transaction---------
        self.issue_item_transaction_data_1 = {
            'issue_to': self.organization_section.id,
            'issue_date': '2022-01-01',
            'item_receiver': 'Test Item Receiver',
            'remarks': None,
            'inventory_transaction_item_set': [
                {
                    'item_batch': self.item_batch.id,
                    'quantity': 10,
                    'is_active': True
                },
                
            ]
        }

        self.issue_item_transaction_data_2 = {
            'issue_to': self.organization_section.id,
            'issue_date': '2022-06-01',
            'item_receiver': 'Test Item Receiver',
            'remarks': None,
            'inventory_transaction_item_set': [
                {
                    'item_batch': self.item_batch.id,
                    'quantity': 120,
                    'is_active': True
                },
               
            ]
        }
        
    

    def test_create_issue_item_inventorytransaction(self):
        url = reverse('issue-item-inventory-transactions-list')  # Replace with the actual name of the URL
        response = self.client.post(url, self.issue_item_transaction_data_1, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(IssueItemInventoryTransaction.objects.count(), 1)
        created_instance = IssueItemInventoryTransaction.objects.first()
        self.assertEqual(created_instance.issue_to, self.organization_section)  # Check that the created instance has the correct issueTo
        
    
    def test_get_issue_transactions(self):
        url = reverse('issue-item-inventory-transactions-list')
        
        response = self.client.post(url, self.issue_item_transaction_data_1, format='json')
        response = self.client.post(url, self.issue_item_transaction_data_2, format='json')

        response = self.client.get(url)
  
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Check that two instances are returned
       


    def tests_get_issue_transactions(self):
      
        url = reverse('issue-item-inventory-transactions-list')
        response = self.client.post(url, self.issue_item_transaction_data_1, format='json')
       
        id=response.data['id']
        url = reverse('issue-item-inventory-transactions-detail', kwargs={'pk': id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], id)  # Check that the returned instance has the correct id


    
    def test_filter_issue_inventory_transaction(self):
     
        url = reverse('issue-item-inventory-transactions-list')
        
        post_response_1=self.client.post(url, self.issue_item_transaction_data_1, format='json')
        post_response_2 = self.client.post(url, self.issue_item_transaction_data_2, format='json')
        # print(post_response_1.data) 
      
        id=post_response_1.data['id']
        url = reverse('issue-item-inventory-transactions-detail', kwargs={'pk': id})
        response_get = self.client.get(url)
        
        
        url = reverse('issue-item-inventory-transactions-list') + '?issue_to=TOS'
        filtered_response = self.client.get(url)
        
       
       
        self.assertEqual(filtered_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(filtered_response.data), 2)  # Check that one instance is returned
      


    def test_filter_issue_inventorytransaction_by_date(self):
   
        url = reverse('issue-item-inventory-transactions-list')
        
        self.client.post(url, self.issue_item_transaction_data_1, format='json')
        self.client.post(url, self.issue_item_transaction_data_2, format='json')

        # Test filtering by an exact date
        response = self.client.get(reverse('issue-item-inventory-transactions-list'), {'issue_date': '2022-01-01'})
      
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data),1)
        self.assertEqual(response.data[0]['issue_date'], '2022-01-01')

        # # Test filtering by a range of dates
        response = self.client.get(reverse('issue-item-inventory-transactions-list'), {'issue_date_from': '2022-01-01', 'issue_date_to': '2022-04-01'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

         # Test filtering by a range of dates
        response = self.client.get(reverse('issue-item-inventory-transactions-list'), {'issue_date_from': '2022-02-01', 'issue_date_to': '2022-06-01'})
     
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)