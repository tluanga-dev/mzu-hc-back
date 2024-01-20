from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import MedicineDosageDuration
from .serializers import MedicineDosageDurationSerializer

class MedicineDosageDurationTestCase(TestCase):
    def setUp(self):

        self.medicine_dosage_duration = MedicineDosageDuration.objects.create(days=7, name="One Week", updated_on="2022-01-01T00:00:00Z")
        

    def test_medicine_dosage_duration_model(self):
        medicine_dosage_duration = MedicineDosageDuration.objects.get(id=self.medicine_dosage_duration.id)
        self.assertEqual(medicine_dosage_duration.days, 7)
        self.assertEqual(medicine_dosage_duration.name, "One Week")

   
    def test_medicine_dosage_duration_viewset(self):
        client = APIClient()
        response = client.get('/item/medicine_dosage_duration/')  # replace with your actual url
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], str(self.medicine_dosage_duration.id))

    def test_medicine_dosage_duration_serializer(self):
        serializer = MedicineDosageDurationSerializer(self.medicine_dosage_duration)
        expected_data = {'id': str(self.medicine_dosage_duration.id), 'days': 7, 'name': "One Week", 'updated_on': "2022-01-01T00:00:00Z"}
        actual_data = serializer.data
        self.assertEqual(actual_data['id'], expected_data['id'])
        self.assertEqual(actual_data['days'], expected_data['days'])
        self.assertEqual(actual_data['name'], expected_data['name'])