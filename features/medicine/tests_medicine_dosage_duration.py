# tests.py


from django.urls import reverse

from rest_framework import status

from features.base.base_test_setup_class import BaseTestCase
from features.item.models import Item
from features.medicine.models import MedicineDosage, MedicineDosageDuration
from features.medicine.serializers import MedicineDosageDurationSerializer

class MedicineDosageDurationModelTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        Item.objects.all().delete()
        self.item = Item.objects.create(
            name="Test Item",
            description="Test Description",
            type=self.item_type,
            unit_of_measurement=self.unit_of_measurement,
            is_active=True
        )
        self.medicine_dosage = MedicineDosage.objects.create(quantity_in_one_take=1, how_many_times_in_a_day=3, name="Test Dosage", item=self.item)
        print('medicine dosage', self.medicine_dosage.item.name)
        self.medicine_dosage_duration = MedicineDosageDuration.objects.create(days=7, name="One Week", medicine_dosage=self.medicine_dosage)

    def test_medicine_dosage_duration_creation(self):
        self.assertEqual(MedicineDosageDuration.objects.count(), 1)
        self.assertEqual(MedicineDosageDuration.objects.get().name, "One Week")

class MedicineDosageDurationViewSetTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        Item.objects.all().delete()
        self.item = Item.objects.create(
            name="Test Item",
            description="Test Description",
            type=self.item_type,
            unit_of_measurement=self.unit_of_measurement,
            is_active=True
        )
        self.medicine_dosage = MedicineDosage.objects.create(quantity_in_one_take=1, how_many_times_in_a_day=3, name="Test Dosage", item=self.item)
        self.medicine_dosage_duration = MedicineDosageDuration.objects.create(days=7, name="One Week", medicine_dosage=self.medicine_dosage)
        self.url = reverse('medicinedosageduration-list')

    def test_get_all_medicine_dosage_durations(self):
        response = self.client.get(self.url)
        medicine_dosage_durations = MedicineDosageDuration.objects.all()
        serializer = MedicineDosageDurationSerializer(medicine_dosage_durations, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_single_medicine_dosage_duration(self):
        url = reverse('medicinedosageduration-detail', kwargs={'pk': self.medicine_dosage_duration.pk})
        response = self.client.get(url)
        serializer = MedicineDosageDurationSerializer(self.medicine_dosage_duration)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_medicine_dosage_duration(self):
        data = {
            'days': 7,
            'name': 'One Week',
            'medicine_dosage': self.medicine_dosage.pk
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_medicine_dosage_duration(self):
        data = {
            'days': 7,
            'name': 'One Week',
            'medicine_dosage': self.medicine_dosage.pk
        }
        url = reverse('medicinedosageduration-detail', kwargs={'pk': self.medicine_dosage_duration.pk})
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_medicine_dosage_duration(self):
        url = reverse('medicinedosageduration-detail', kwargs={'pk': self.medicine_dosage_duration.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)