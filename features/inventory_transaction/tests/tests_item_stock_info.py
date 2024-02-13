from django.utils import timezone
import datetime
from features.base.base_test_setup_class import BaseTestCase
from features.inventory_transaction.models import IndentInventoryTransaction, InventoryTransaction, InventoryTransactionItem, IssueItemInventoryTransaction, ItemStockInfo
from features.inventory_transaction.serializers import IndentInventoryTransactionSerializer
from features.item.models import Item, ItemBatch
from features.organisation_section.models import OrganisationSection
from features.supplier.models import Supplier



class ItemStockInfoModelTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        super().setUp()
        IndentInventoryTransaction.objects.all().delete()  
        InventoryTransactionItem.objects.all().delete()
        IssueItemInventoryTransaction.objects.all().delete()
        ItemStockInfo.objects.all().delete()
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
            date_of_expiry=datetime.date.today(),
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
                    'item_batch': self.item_batch.id,
                    'quantity': 100,
                    'is_active': True,
                    'iventory_transaction_type': 'itemIssue'
                },
               
            ]
        }
       
    def test_read_item_stock_info(self):
      
        
   
        self.assertEqual(ItemStockInfo.objects.count(), 1)

        self.assertEqual(ItemBatch.objects.count(), 1)
        self.assertEqual(self.item_batch.batch_id, 'test')

    