from django.test import TestCase
from .models import Supplier

class SupplierModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Supplier.objects.create(name='Test Supplier', contact_no=1234567890.0, email='test@example.com', 
                                address='Test Address', remarks='Test Remarks', is_active=True)

    def test_name_label(self):
        supplier = Supplier.objects.get(id=1)
        field_label = supplier._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_contact_no_label(self):
        supplier = Supplier.objects.get(id=1)
        field_label = supplier._meta.get_field('contact_no').verbose_name
       
        self.assertEqual(field_label,'contact no')

    def test_email_label(self):
        supplier = Supplier.objects.get(id=1)
        field_label = supplier._meta.get_field('email').verbose_name
        self.assertEqual(field_label, 'email')

    def test_address_label(self):
        supplier = Supplier.objects.get(id=1)
        field_label = supplier._meta.get_field('address').verbose_name
        self.assertEqual(field_label, 'address')

    def test_remarks_label(self):
        supplier = Supplier.objects.get(id=1)
        field_label = supplier._meta.get_field('remarks').verbose_name
        self.assertEqual(field_label, 'remarks')

    def test_is_active_label(self):
        supplier = Supplier.objects.get(id=1)
        field_label = supplier._meta.get_field('is_active').verbose_name
        self.assertEqual(field_label, 'is active')

    def test_created_on_label(self):
        supplier = Supplier.objects.get(id=1)
        field_label = supplier._meta.get_field('created_on').verbose_name
        self.assertEqual(field_label, 'created on')

    def test_updated_on_label(self):
        supplier = Supplier.objects.get(id=1)
        field_label = supplier._meta.get_field('updated_on').verbose_name
        self.assertEqual(field_label, 'updated on')

    def test_name_max_length(self):
        supplier = Supplier.objects.get(id=1)
        max_length = supplier._meta.get_field('name').max_length
        self.assertEqual(max_length, 255)

    def test_object_name_is_name(self):
        supplier = Supplier.objects.get(id=1)
     
        expected_object_name = f'{supplier.name}'
   
        self.assertEqual(expected_object_name, str(supplier.name))