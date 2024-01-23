# # tests.py

# from django.test import TestCase
# from rest_framework.test import APIClient
# from rest_framework import status
# from .models import MedicineDosageDuration
# from .serializers import MedicineDosageDurationSerializer

# class MedicineDosageDurationModelTestCase(TestCase):
#     def setUp(self):
#         self.medicine_dosage_duration = MedicineDosageDuration.objects.create(days=7, name="One Week")

#     def test_medicine_dosage_duration_creation(self):
#         self.assertEqual(MedicineDosageDuration.objects.count(), 1)
#         self.assertEqual(MedicineDosageDuration.objects.get().name, "One Week")

# class MedicineDosageDurationViewSetTestCase(TestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.medicine_dosage_duration = MedicineDosageDuration.objects.create(days=7, name="One Week")

#     def test_medicine_dosage_duration_list(self):
#         response = self.client.get('/medicine/medicine_dosage_duration/')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 1)

# class MedicineDosageDurationSerializerTestCase(TestCase):
#     def setUp(self):
#         self.medicine_dosage_duration = MedicineDosageDuration.objects.create(days=7, name="One Week")
#         self.serializer = MedicineDosageDurationSerializer(instance=self.medicine_dosage_duration)

#     def test_contains_expected_fields(self):
#         data = self.serializer.data
#         self.assertCountEqual(data.keys(), ['id', 'days', 'name', 'item', 'updated_on'])