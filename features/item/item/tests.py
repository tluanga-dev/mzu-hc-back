# tests.py

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Item, ItemType
from .serializers import ItemSerializer

class ItemModelTestCase(TestCase):
    def setUp(self):
        self.item_type = ItemType.objects.create(name="Test Type")
        self.item = Item.objects.create(name="Test Item", description="Test Description", type=self.item_type)

    def test_item_creation(self):
        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(Item.objects.get().name, "Test Item")

class ItemViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.item_type = ItemType.objects.create(name="Test Type")
        self.item = Item.objects.create(name="Test Item", description="Test Description", type=self.item_type)

    def test_item_list(self):
        response = self.client.get('/item/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

class ItemSerializerTestCase(TestCase):
    def setUp(self):
        self.item_type = ItemType.objects.create(name="Test Type")
        self.item = Item.objects.create(name="Test Item", description="Test Description", type=self.item_type)
        self.serializer = ItemSerializer(instance=self.item)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertCountEqual(data.keys(), ['id', 'name', 'description', 'type', 'is_active', 'created_on', 'updated_on'])