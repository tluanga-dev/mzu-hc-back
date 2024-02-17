# from django.urls import reverse
# from rest_framework import status
# from rest_framework.test import APITestCase, APIClient
# from .models import Supplier
# from .serializers import SupplierSerializer

# class SupplierViewSetTestCase(APITestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.supplier = Supplier.objects.create(name='Test Supplier', contact_no=1234567890.0, email='test@example.com', address='Test Address', remarks='Test Remarks', is_active=True)
#         self.url = reverse('supplier-list')

#     def test_get_all_suppliers(self):
#         response = self.client.get(self.url)
#         suppliers = Supplier.objects.all()
#         serializer = SupplierSerializer(suppliers, many=True)
#         self.assertEqual(response.data, serializer.data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     def test_get_single_supplier(self):
#         response = self.client.get(reverse('supplier-detail', kwargs={'pk': self.supplier.pk}))
#         supplier = Supplier.objects.get(pk=self.supplier.pk)
#         serializer = SupplierSerializer(supplier)
#         self.assertEqual(response.data, serializer.data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     def test_create_supplier(self):
#         data = {'name': 'New Supplier', 'contact_no': 9876543210.0, 'email': 'new@example.com', 'address': 'New Address', 'remarks': 'New Remarks', 'is_active': True}
#         response = self.client.post(self.url, data)
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)

#     def test_update_supplier(self):
#         data = {'name': 'Updated Supplier', 'contact_no': 9876543210.0, 'email': 'updated@example.com', 'address': 'Updated Address', 'remarks': 'Updated Remarks', 'is_active': True}
#         response = self.client.put(reverse('supplier-detail', kwargs={'pk': self.supplier.pk}), data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     def test_delete_supplier(self):
#         response = self.client.delete(reverse('supplier-detail', kwargs={'pk': self.supplier.pk}))
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)