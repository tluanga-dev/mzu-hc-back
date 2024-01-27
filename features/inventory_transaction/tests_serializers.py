from datetime import date
from django.test import TestCase
from features.base.base_test_setup_class import BaseTestCase
from features.item.item.models import Item
from features.item.item_category.models import ItemCategory
from features.item.item_type.models import ItemType
from features.item.unit_of_measurement.models import UnitOfMeasurement

from features.supplier.models import Supplier
from .models import InventoryTransactionItem, IndentInventoryTransaction,  ItemBatch
from .serializers import IndentInventoryTransactionSerializer

class IndentInventoryTransactionSerializerTestCase(BaseTestCase):
    def setUp(self):
        self.item_category = ItemCategory.objects.create(
            name="Test Category",
            abbreviation="TC",
            description="Test Description",
            is_active=True
        )
        self.item_type = ItemType.objects.create(
            name="Test Type",
            abbreviation="TT",
            description="Test Description",
            example="Test Example",
            category=self.item_category,
            is_active=True
        )
        self.unit_of_measurement = UnitOfMeasurement.objects.create(
            name="Test Unit",
            abbreviation="TU",
            description="Test Description",
            example="Test Example",
            is_active=True
        )
  
        self.item = Item.objects.create(
            name="Test Item",
            description="Test Description",
            type=self.item_type,
            unit_of_measurement=self.unit_of_measurement,
            is_active=True
        )
        self.supplier=Supplier.objects.create(
            name='Test Supplier', 
            address='Test Address', 
            contact_no='1234567890',
            email='test@gmail.com'
        )
        self.item_batch1=ItemBatch.objects.create(
            batch_id='B2',
            description='Test Batch 1',
            date_of_expiry=date.today(),
            item=self.item
        )
        self.item_batch2 =ItemBatch.objects.create(
            batch_id='B2',
            description='Test Batch2',
            date_of_expiry=date.today(),
            item=self.item
        )
        self.indent_transaction = IndentInventoryTransaction.objects.create(
            inventory_transaction_type='indent',
            iventory_transaction_id='INDENT1',
            status='pending',
            supplier=self.supplier,
            supplyOrderNo='SO1',
            supplyOrderDate='2022-01-01',
            dateOfDeliverty='2022-01-01'
        )
        


        self.transaction_item1 = InventoryTransactionItem.objects.create(
            inventory_transaction=self.indent_transaction,
            item_batch=self.item_batch1,
            quantity=10,
            is_active=True
        )
        self.transaction_item2 = InventoryTransactionItem.objects.create(
            inventory_transaction=self.indent_transaction,
            item_batch=self.item_batch2,
            quantity=5,
            is_active=True
        )

    def test_serializer(self):
        serializer = IndentInventoryTransactionSerializer(self.indent_transaction)
 
         # Exclude 'date_time', 'created_on', and 'updated_on' fields from the comparison
        serialized_data = serializer.data
        

        for item in serialized_data['inventorytransactionitem_set']:
            item.pop('created_on', None)
            item.pop('updated_on', None)
        serialized_data.pop('date_time', None)
        print('------Serializer Data------')
        print(serializer.data) 
        print('------Expected Data------')
        expected_data = {
            'id': self.indent_transaction.id,
            'inventory_transaction_type': 'indent',
            'iventory_transaction_id': 'INDENT1',
            'status': 'pending',
            
            'supplier': {
                'id': 8, 
                'name': 'Test Supplier',
                'contact_no': '1234567890', 
                'email': 'test@gmail.com', 
                'address': 'Test Address', 
                'remarks': None, 
                'is_active': True
            },

            'supplyOrderNo': 'SO1',
            'supplyOrderDate': '2022-01-01',
            'dateOfDeliverty': '2022-01-01',
            'remarks': None,
            'date_time': self.indent_transaction.date_time.isoformat(),
            'inventorytransactionitem_set': [
                {
                    'id': self.transaction_item1.id,
                    'inventory_transaction': self.indent_transaction.id,
                    'item_batch': self.item_batch1.id,
                    'quantity': 10,
                    'is_active': True,
                    'created_on': self.transaction_item1.created_on.isoformat(),
                    'updated_on': self.transaction_item1.updated_on.isoformat(),
                },
                {
                    'id': self.transaction_item2.id,
                    'inventory_transaction': self.indent_transaction.id,
                    'item_batch': self.item_batch2.id,
                    'quantity': 5,
                    'is_active': True,
                    'created_on': self.transaction_item2.created_on.isoformat(),
                    'updated_on': self.transaction_item2.updated_on.isoformat(),
                }
            ]
        }
        print(expected_data)
        print('-----')
        self.assertEqual(serializer.data, expected_data)
            