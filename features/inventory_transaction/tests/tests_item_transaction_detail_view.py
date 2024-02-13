from datetime import date
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from features.base.base_test_setup_class import BaseTestCase
from features.inventory_transaction.models import IndentInventoryTransaction, InventoryTransaction, InventoryTransactionItem
from features.inventory_transaction.serializers import IndentInventoryTransactionSerializer, IssueItemInventoryTransactionSerializer

from features.item.models import Item, ItemBatch
from features.organisation_section.models import OrganisationSection
from features.supplier.models import Supplier


class ItemTransactionsViewTestCase(BaseTestCase):
    def setUp(self):
        # Create an Item instance
        super().setUp()
        OrganisationSection.objects.all().delete()
        Item.objects.all().delete()
        self.item = Item.objects.create(
            name="Test Item",
            description="Test Description",
            type=self.item_type,
            unit_of_measurement=self.unit_of_measurement,
            is_active=True
        )
        
        self.item.save()
        print('---------')
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
        serializer=IssueItemInventoryTransactionSerializer(data=self.issue_item_transaction_data)
        if(serializer.is_valid()):
            serializer.save()
        else:
            print('serializer is not valid')
            print(serializer.errors)
        # create indent transaction




    def test_get_item_transactions(self):
        url = reverse('item-transactions-detail', kwargs={'pk': self.item.id})
        response = self.client.get(url)
        print(response.data)
        

        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(response.data['item']['id'], str(self.item.id))
        # self.assertEqual(response.data['item_stock_info']['stock'], self.item_stock_info.stock)
        # self.assertEqual(response.data['transactions'][0]['quantity'], self.transaction.quantity)