from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import UnitOfMeasurement

class UnitOfMeasurementModelTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a unit of measurement
        UnitOfMeasurement.objects.create(name='Test', abbreviation='T', description='Test Unit', example='Example', is_active=True)

    def test_create_unit_of_measurement(self):
        """
        Ensure we can create a new unit of measurement object.
        """
        url = reverse('unitofmeasurement-list')
        data = {'name': 'Test2', 'abbreviation': 'T2', 'description': 'Test Unit 2', 'example': 'Example 2', 'is_active': True}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(UnitOfMeasurement.objects.count(), 2)
        self.assertEqual(UnitOfMeasurement.objects.get(id=2).name, 'Test2')

    def test_get_unit_of_measurement(self):
        """
        Ensure we can get a unit of measurement object.
        """
        url = reverse('unitofmeasurement-detail', args=[1])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test')