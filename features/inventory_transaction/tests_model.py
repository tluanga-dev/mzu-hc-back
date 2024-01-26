from django.test import TestCase

from features.base.base_test_setup_class import BaseTestCase
from features.supplier.models import Supplier
from .models import IndentInventoryTransaction, InventoryTransaction
from datetime import date

class IndentInventoryTransactionModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        super().setUpTestData()
        print('--------Creating Indent Transaction--')
        cls.supplier=Supplier.objects.create(
            name='Test Supplier', 
            address='Test Address', 
            contact_no='1234567890',
            email='test@gmail.com'
        )


        cls.indent_transaction = IndentInventoryTransaction.objects.create(
            inventory_transaction_type=InventoryTransaction.INDENT,
            quantity=10,
            supplier=cls.supplier, 
            supplyOrderNo='12345', 
            supplyOrderDate=date.today(), 
            dateOfDeliverty=date.today()
        )
        print('--------Created Indent Transaction--')
        # print(cls.indent_transaction)
    def test_creation(self):

        
        self.assertEqual(Supplier.objects.count(), 1)
        self.assertEqual(IndentInventoryTransaction.objects.count(), 1)

    def test_requested_quantity_label(self):
        indenttransaction = IndentInventoryTransaction.objects.get(id=1)
        field_label = indenttransaction._meta.get_field('quantity').verbose_name
        self.assertEquals(field_label, 'quantity')

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