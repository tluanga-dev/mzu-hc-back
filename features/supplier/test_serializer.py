from django.test import TestCase
from features.supplier.models import Supplier
from features.supplier.serializers import SupplierSerializer


class SupplierSerializerTest(TestCase):
    def setUp(self):
        self.supplier_attributes = {
            'name': 'Test Supplier',
            'contact': 1234567890.0,
            'email': 'test@example.com',
            'address': 'Test Address',
            'remarks': 'Test Remarks',
            'is_active': True
        }

        self.supplier = Supplier.objects.create(**self.supplier_attributes)
        self.serializer_data = SupplierSerializer(self.supplier).data
      

    def test_contains_expected_fields(self):

        self.assertEqual(set(self.serializer_data.keys()), set([
            'id',
            'name', 
            'contact', 
            'email',
            'address',
            'remarks',
            'is_active',
            'created_on',
            'updated_on',
        ]))
    def test_name_field_content(self):
        data = SupplierSerializer(Supplier(name='Test Supplier')).data
        self.assertEqual(data['name'], 'Test Supplier')

    def test_contact_field_content(self):
        data = SupplierSerializer(Supplier(contact=1234567890.0)).data
        self.assertEqual(data['contact'], 1234567890.0)

    def test_email_field_content(self):
        data = SupplierSerializer(Supplier(email='test@example.com')).data
        self.assertEqual(data['email'], 'test@example.com')

    def test_address_field_content(self):
        data = SupplierSerializer(Supplier(address='Test Address')).data
        self.assertEqual(data['address'], 'Test Address')

    def test_remarks_field_content(self):
        data = SupplierSerializer(Supplier(remarks='Test Remarks')).data
        self.assertEqual(data['remarks'], 'Test Remarks')

    def test_is_active_field_content(self):
        data = SupplierSerializer(Supplier(is_active=True)).data
        self.assertEqual(data['is_active'], True)

    def test_validation(self):
        serializer = SupplierSerializer(data=self.supplier_attributes)
        self.assertTrue(serializer.is_valid(raise_exception=True))