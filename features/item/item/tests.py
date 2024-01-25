# tests.py

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from features.base.base_test_setup_class import BaseTestCase
from features.item.item_category.models import ItemCategory

from features.item.unit_of_measurement.models import UnitOfMeasurement
from .models import Item, ItemType
from .serializers import ItemSerializer

class ItemModelTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.item = Item.objects.create(
            name="Test Item",
            description="Test Description",
            type=self.item_type,
            unit_of_measurement=self.unit_of_measurement,
            is_active=True
        )
       
    def test_item_creation(self):
        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(Item.objects.get().name, "Test Item")


class ItemSerializerTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.item = Item.objects.create(
            name="Test Item",
            description="Test Description",
            type=self.item_type,
            unit_of_measurement=self.unit_of_measurement,
            is_active=True
        )
        self.serializer = ItemSerializer(instance=self.item)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertCountEqual(data.keys(), ['id', 'name', 'description', 'type', 'is_active', 'created_on', 'updated_on'])

class ItemViewSetTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.client = APIClient()
        Item.objects.all().delete()
        # ---We need to delete all Item objects created before
        self.item = Item.objects.create(
            name="Test Item",
            description="Test Description",
            type=self.item_type,
            unit_of_measurement=self.unit_of_measurement,
            is_active=True
        )
        return super().setUp()
    
    def test_item_list(self):
        response = self.client.get('/item/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
 
        self.assertEqual(len(response.data), 1)
