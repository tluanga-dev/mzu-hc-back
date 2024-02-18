from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from features.item.models import UnitOfMeasurement


class UnitOfMeasurementModelTest(APITestCase):
    @classmethod
    def setUp(self):
        # Create a unit of measurement
    
        self.unit_of_measurement=UnitOfMeasurement.objects.create(name='Test', abbreviation='T', description='Test Unit', example='Example')

    def test_create_unit_of_measurement(self):
        """
        Ensure we can create a new unit of measurement object.
        """
        UnitOfMeasurement.objects.all().delete()
        url = reverse('unit-of-measurement-list')
        data = {'name': 'Test2', 'abbreviation': 'T2', 'description': 'Test Unit 2', 'example': 'Example 2', 'is_active': True}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(UnitOfMeasurement.objects.count(), 1)
        self.assertEqual(UnitOfMeasurement.objects.get(name='Test2').name, 'Test2')

    def test_get_unit_of_measurement(self):
        """
        Ensure we can get a unit of measurement object.
        """
        url = reverse('unit-of-measurement-detail', args=[str(self.unit_of_measurement.id)])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test')