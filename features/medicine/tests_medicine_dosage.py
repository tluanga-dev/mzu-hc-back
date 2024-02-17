# # tests.py

# from django.test import TestCase
# from rest_framework.test import APIClient
# from rest_framework import status
# from features.base.base_test_setup_class import BaseTestCase
# from features.item.models import Item
# from features.medicine.models import MedicineDosage



# from .serializers import MedicineDosageSerializer

# class MedicineDosageModelTestCase(BaseTestCase):

#     def setUp(self):
#         super().setUp()

#         self.item = Item.objects.create(
#             name="Test Item",
#             description="Test Description",
#             type=self.item_type,
#             unit_of_measurement=self.unit_of_measurement,
#             is_active=True
#         )
        
#         self.medicine_dosage = MedicineDosage.objects.create(quantity_in_one_take=1, how_many_times_in_a_day=3, name="Test Dosage", item=self.item)

#     def test_medicine_dosage_creation(self):
#         self.assertEqual(MedicineDosage.objects.count(), 1)
#         self.assertEqual(MedicineDosage.objects.get().name, "Test Dosage")

# class MedicineDosageViewSetTestCase(BaseTestCase):
#     def setUp(self):
#         super().setUp()
#         Item.objects.all().delete()
#         self.item = Item.objects.create(
#             name="Test Item",
#             description="Test Description",
#             type=self.item_type,
#             unit_of_measurement=self.unit_of_measurement,
#             is_active=True
#         )
#         self.medicine_dosage = MedicineDosage.objects.create(quantity_in_one_take=1, how_many_times_in_a_day=3, name="Test Dosage", item=self.item)

#     def test_medicine_dosage_list(self):
#         response = self.client.get('/medicine/medicine_dosage/')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 1)

# class MedicineDosageSerializerTestCase(BaseTestCase):
#     def setUp(self):
#         super().setUp()
#         Item.objects.all().delete()
#         self.item = Item.objects.create(
#             name="Test Item",
#             description="Test Description",
#             type=self.item_type,
#             unit_of_measurement=self.unit_of_measurement,
#             is_active=True
#         )
#         self.medicine_dosage = MedicineDosage.objects.create(
#             quantity_in_one_take=1,
#             how_many_times_in_a_day=2,
#             name="Test Medicine Dosage",
#             item=self.item
#         )
      
#         self.serializer = MedicineDosageSerializer(instance=self.medicine_dosage)

#     def test_contains_expected_fields(self):
#         data = self.serializer.data
#         self.assertCountEqual(data.keys(), ['id', 'quantity_in_one_take', 'how_many_times_in_a_day', 'name', 'item', 'updated_on'])

#     def test_content(self):
#         data = self.serializer.data
        
#         self.assertEqual(data['quantity_in_one_take'], self.medicine_dosage.quantity_in_one_take)
#         self.assertEqual(data['how_many_times_in_a_day'], self.medicine_dosage.how_many_times_in_a_day)
#         self.assertEqual(data['name'], self.medicine_dosage.name)
#         self.assertEqual(data['item'], self.medicine_dosage.item.id)
#         self.assertEqual(data['updated_on'], self.medicine_dosage.updated_on.strftime('%Y-%m-%dT%H:%M:%S.%fZ'))