from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from features.item.item_category.models import ItemCategory
from features.item.unit_of_measurement.models import UnitOfMeasurement
from .models import Item, ItemType
from .serializers import ItemSerializer

class ItemTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.item_category = ItemCategory.objects.create(
            name="Test Category",
            abbreviation="TC",
            description="Test Description",
            is_active=True
        )
        self.item_type = ItemType.objects.create(
            name="Test Type",
            abbreviation="TT",
            description="Test Description",
            example="Test Example",
            category=self.item_category,
            is_active=True
        )
        self.unit_of_measurement = UnitOfMeasurement.objects.create(
            name="Test Unit",
            abbreviation="TU",
            description="Test Description",
            example="Test Example",
            is_active=True
        )
        self.item = Item.objects.create(
            name="Test Item",
            description="Test Description",
            type=self.item_type,
            unit_of_measurement=self.unit_of_measurement,
            is_active=True
        )
        self.serializer = ItemSerializer(instance=self.item)

    def test_item_creation(self):
        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(Item.objects.get().name, "Test Item")

    def test_item_list(self):
        response = self.client.get('/item/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertCountEqual(data.keys(), ['id', 'name', 'description', 'type', 'is_active', 'created_on', 'updated_on'])