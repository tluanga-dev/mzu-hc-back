# # tests.py

# from django.test import TestCase
# from rest_framework.test import APIClient
# from rest_framework import status
# from features.item.item.models import Item

# from features.item.item_category.models import ItemCategory
# from features.item.item_type.models import ItemType
# from features.item.unit_of_measurement.apps import UnitOfMeasurementConfig
# from .models import MedicineDosage
# from .serializers import MedicineDosageSerializer

# class MedicineDosageModelTestCase(TestCase):

#     def setUp(self):
#         item_category = ItemCategory.objects.create(
#             name="Test Category",
#             abbreviation="TC",
#             description="Test Description",
#             is_active=True
#         )
#         item_type = ItemType.objects.create(
#             name="Test Type",
#             abbreviation="TT",
#             description="Test Description",
#             example="Test Example",
#             category=item_category,
#             is_active=True
#         )
#         unit_of_measurement = UnitOfMeasurementConfig.objects.create(
#             name="Test Unit",
#             abbreviation="TU",
#             description="Test Description",
#             example="Test Example",
#             is_active=True
#         )
#         self.item = Item.objects.create(
#             name="Test Item",
#             description="Test Description",
#             type=item_type,
#             unit_of_measurement=unit_of_measurement,
#             is_active=True
#         )
#         self.medicine_dosage = MedicineDosage.objects.create(
#             item=self.item,
#             quantity_in_one_take=1,
#             how_many_times_in_a_day=3,
#             name="Test Dosage"
#         )

 

#     def test_medicine_dosage_creation(self):
#         self.assertEqual(MedicineDosage.objects.count(), 1)
#         self.assertEqual(MedicineDosage.objects.get().name, "Test Dosage")

# class MedicineDosageViewSetTestCase(TestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.medicine_dosage = MedicineDosage.objects.create(quantity_in_one_take=1, how_many_times_in_a_day=3, name="Test Dosage")

#     def test_medicine_dosage_list(self):
#         response = self.client.get('/medicine_dosage/')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 1)

# class MedicineDosageSerializerTestCase(TestCase):
#     def setUp(self):
#         self.medicine_dosage = MedicineDosage.objects.create(quantity_in_one_take=1, how_many_times_in_a_day=3, name="Test Dosage")
#         self.serializer = MedicineDosageSerializer(instance=self.medicine_dosage)

#     def test_contains_expected_fields(self):
#         data = self.serializer.data
#         self.assertCountEqual(data.keys(), ['id', 'quantity_in_one_take', 'how_many_times_in_a_day', 'name', 'item', 'medicine_dosage', 'updated_on'])