from features.base.base_test_setup_class import BaseTestCase
from features.id_manager.models import IdManager
from features.inventory_transaction.indent_transaction.models import IndentInventoryTransaction
from features.inventory_transaction.inventory_transaction.models import InventoryTransaction, InventoryTransactionItem
from features.item.models import Item, ItemBatch
from features.supplier.models import Supplier
from datetime import date

class IndentInventoryTransactionModelTest(BaseTestCase):
    counter = 0  # Add a class-level counter
    def setUp(self):
        # Set up non-modified objects used by all test methods
        super().setUp()
        Item.objects.all().delete()
        Supplier.objects.all().delete()
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
            supply_order_no=IndentInventoryTransactionModelTest.counter, 
            supply_order_date=date.today(), 
            date_of_delivery=date.today()
        )
       
       
        IndentInventoryTransactionModelTest.counter += 1 


    def test_creation(self):
        
        self.assertEqual(Supplier.objects.count(), 1)
        self.assertEqual(IndentInventoryTransaction.objects.count(), 1)


    def test_supplier_label(self):
        indent_transaction = IndentInventoryTransaction.objects.get(id=self.indent_transaction.id)
        field_label = indent_transaction._meta.get_field('supplier').name
        self.assertEquals(field_label, 'supplier')

    def test_supply_order_no_label(self):
        indenttransaction = IndentInventoryTransaction.objects.get(id=self.indent_transaction.id)
        field_label = indenttransaction._meta.get_field('supply_order_no').name

        self.assertEquals(field_label, 'supply_order_no')

    def test_supply_order_date_label(self):
        indent_transaction = IndentInventoryTransaction.objects.get(id=self.indent_transaction.id)
        field_label = indent_transaction._meta.get_field('supply_order_date').name
     
     
        self.assertEquals(field_label, 'supply_order_date')

    def test_date_of_delivery_label(self):
        indenttransaction = IndentInventoryTransaction.objects.get(id=self.indent_transaction.id)
        field_label = indenttransaction._meta.get_field('date_of_delivery').name
        self.assertEquals(field_label, 'date_of_delivery')

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
        
        self.assertEqual(InventoryTransactionItem.objects.count(), 1)
        
        indenttransaction_from_db = IndentInventoryTransaction.objects.get(id=self.indent_transaction.id)

        transaction_items = indenttransaction_from_db.inventory_transaction_item_set.all()

        self.assertEqual(transaction_items.count(), 1)

