from django.test import TestCase

from features.base.base_test_setup_class import BaseTestCase
from features.id_manager.models import IdManager
from features.item.models import Item, ItemBatch
from features.supplier.models import Supplier
from .models import IndentInventoryTransaction, InventoryTransaction, InventoryTransactionItem
from datetime import date

class IndentInventoryTransactionModelTest(BaseTestCase):
    counter = 0  # Add a class-level counter

    
    def setUp(self):
        # Set up non-modified objects used by all test methods
        super().setUp()
        Item.objects.all().delete()
        self.supplier=Supplier.objects.create(
            name='Test Supplier', 
            address='Test Address', 
            contact_no='1234567890',
            email='test@gmail.com'
        )

        InventoryTransactionItem.objects.all().delete() 
        self.indent_transaction = IndentInventoryTransaction.objects.create(
            inventory_transaction_type=InventoryTransaction.TransactionTypes.INDENT,
            inventory_transaction_id=IdManager.generateId(prefix='INDENT'),
            supplier=self.supplier, 
            supplyOrderNo=IndentInventoryTransactionModelTest.counter, 
            supplyOrderDate=date.today(), 
            dateOfDeliverty=date.today()
        )
       
        # print(cls.indent_transaction)
        IndentInventoryTransactionModelTest.counter += 1 
    def test_creation(self):
        
        self.assertEqual(Supplier.objects.count(), 1)
        self.assertEqual(IndentInventoryTransaction.objects.count(), 1)

    def test_indent_transaction(self):
        print('Indent Transaction')
   

   

    def test_supplier_label(self):
        indenttransaction = IndentInventoryTransaction.objects.get(id=1)
        field_label = indenttransaction._meta.get_field('supplier').verbose_name
        self.assertEquals(field_label, 'supplier')

    def test_supplyOrderNo_label(self):
        indenttransaction = IndentInventoryTransaction.objects.get(id=1)
        field_label = indenttransaction._meta.get_field('supplyOrderNo').verbose_name
        self.assertEquals(field_label, 'supplyOrderNo')

    def test_supplyOrderDate_label(self):
        indenttransaction = IndentInventoryTransaction.objects.get(id=1)
        field_label = indenttransaction._meta.get_field('supplyOrderDate').verbose_name
        self.assertEquals(field_label, 'supplyOrderDate')

    def test_dateOfDeliverty_label(self):
        indenttransaction = IndentInventoryTransaction.objects.get(id=1)
        field_label = indenttransaction._meta.get_field('dateOfDeliverty').verbose_name
        self.assertEquals(field_label, 'dateOfDeliverty')

    # -------test for the Transaction Item------
    def test_transaction_item_created(self):
        InventoryTransactionItem.objects.all().delete()
        self.item = Item.objects.create(
            name="Test Item",
            description="Test Description",
            type=self.item_type,
            unit_of_measurement=self.unit_of_measurement,
            is_active=True
        )
        self.item_batch=ItemBatch.objects.create(
            batch_id='B2',
            description='Test Batch',
            date_of_expiry=date.today(),
            item=self.item
        )
     
        self.transaction_item = InventoryTransactionItem.objects.create(
            inventory_transaction=self.indent_transaction,
            item_batch=self.item_batch,
            quantity=10
        )
        print(self.transaction_item.inventory_transaction)
        self.assertEqual(InventoryTransactionItem.objects.count(), 1)
        
        indenttransaction_from_db = IndentInventoryTransaction.objects.get(id=1)

        transaction_items = indenttransaction_from_db.inventorytransactionitem_set.all()

        for item in transaction_items:
            print(item.id, item.quantity)  # Or whatever fields you're interested in
        # self.assertEqual(1,transaction_items.count)
        # To get all InventoryTransactionItem objects related to self.indent_transaction,
        #  you can use the reverse relation created by the ForeignKey in the InventoryTransactionItem model. 
        # Here's how you can do it:


        # transaction_items will be a Django QuerySet containing all
        # InventoryTransactionItem objects that are associated with self.indent_transaction.
        #You can iterate over this QuerySet to access each individual InventoryTransactionItem:
