from django.test import TestCase
from features.supplier.models import Supplier
from features.supplier.serializers import SupplierSerializer


class SupplierSerializerTest(TestCase):
    def setUp(self):
        self.supplier_data= {
            'name': 'Test Supplier',
            'contact_no': 1234567890.0,
            'email': 'test@example.com',
            'address': 'Test Address',
            'remarks': 'Test Remarks',
            
        }
        
        self.supplier = Supplier.objects.create(**self.supplier_data)
        self.serializer_data = SupplierSerializer(self.supplier).data
      

    def test_contains_expected_fields(self):

        self.assertEqual(set(self.serializer_data.keys()), set([
            'id',
            'name', 
            'contact_no', 
            'email',
            'address',
            'remarks',
            'is_active',
      
        ]))
    def test_name_field_content(self):
        data = SupplierSerializer(Supplier(name='Test Supplier')).data
        self.assertEqual(data['name'], 'Test Supplier')

    def test_contact_no_field_content(self):
        data = SupplierSerializer(Supplier(contact_no=1234567890.0)).data
        self.assertEqual(data['contact_no'], 1234567890.0)

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
        serializer = SupplierSerializer(data=self.supplier_data)
        self.assertTrue(serializer.is_valid(raise_exception=True))

    def test_create_serializer(self):
        serializer = SupplierSerializer(data=self.supplier_data)
        if(serializer.is_valid()):
            serializer.save()
        else:
            print(serializer.errors)

    def test_serializer_get(self):
        serializer = SupplierSerializer(self.supplier)

        expected_data = {
            'id': str(self.supplier.id),
            'name': self.supplier.name,
            'contact_no': self.supplier.contact_no,
            'email': self.supplier.email,
            'address': self.supplier.address,
            'remarks': self.supplier.remarks,
            'is_active': self.supplier.is_active,
        }
        serializer.data.pop('id', None)
        self.assertEqual(expected_data, serializer.data)
        
    def test_update(self):
        self.supplier = Supplier.objects.create(
            name='Test Supplier',
            contact_no=1234567890,
            email='test@supplier.com',
            address='123 Test St',
            remarks='Test Remarks',
            is_active=True,
        )

        self.serializer = SupplierSerializer(instance=self.supplier)



        data = {
            'name': 'Updated Supplier',
            'contact_no': 9876543210,
            'email': 'updated@supplier.com',
            'address': '321 Updated St',
            'remarks': 'Updated Remarks',
            'is_active': False,
        }

        updated_serializer = self.serializer.update(self.supplier, data)
        updated_supplier = Supplier.objects.get(id=self.supplier.id)

        self.assertEqual(updated_supplier.name, data['name'])
        self.assertEqual(updated_supplier.contact_no, data['contact_no'])
        self.assertEqual(updated_supplier.email, data['email'])
        self.assertEqual(updated_supplier.address, data['address'])
        self.assertEqual(updated_supplier.remarks, data['remarks'])
        self.assertEqual(updated_supplier.is_active, data['is_active'])