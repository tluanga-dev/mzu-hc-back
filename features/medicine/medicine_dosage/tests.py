# tests.py

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import MedicineDosage
from .serializers import MedicineDosageSerializer

class MedicineDosageModelTestCase(TestCase):
    def setUp(self):
        self.medicine_dosage = MedicineDosage.objects.create(quantity_in_one_take=1, how_many_times_in_a_day=3, name="Test Dosage")

    def test_medicine_dosage_creation(self):
        self.assertEqual(MedicineDosage.objects.count(), 1)
        self.assertEqual(MedicineDosage.objects.get().name, "Test Dosage")

class MedicineDosageViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.medicine_dosage = MedicineDosage.objects.create(quantity_in_one_take=1, how_many_times_in_a_day=3, name="Test Dosage")

    def test_medicine_dosage_list(self):
        response = self.client.get('/medicine_dosage/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

class MedicineDosageSerializerTestCase(TestCase):
    def setUp(self):
        self.medicine_dosage = MedicineDosage.objects.create(quantity_in_one_take=1, how_many_times_in_a_day=3, name="Test Dosage")
        self.serializer = MedicineDosageSerializer(instance=self.medicine_dosage)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertCountEqual(data.keys(), ['id', 'quantity_in_one_take', 'how_many_times_in_a_day', 'name', 'item', 'medicine_dosage', 'updated_on'])