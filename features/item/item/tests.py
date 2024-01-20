# Python
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from .models import Item
from .serializers import ItemSerializer
from .views import ItemViewSet

class ModelTestCase(TestCase):
    """This class defines the test suite for the Item model."""

    def setUp(self):
        """Define the test client and other test variables."""
        self.item_name = "Test item"
        self.item = Item(name=self.item_name)

    def test_model_can_create_an_item(self):
        """Test the item model can create an item."""
        old_count = Item.objects.count()
        self.item.save()
        new_count = Item.objects.count()
        self.assertNotEqual(old_count, new_count)

class ViewTestCase(TestCase):
    """Test suite for the api views."""

    def setUp(self):
        """Define the test client and other test variables."""
        self.client = APIClient()
        self.item_data = {'name': 'Test item'}
        self.response = self.client.post(
            reverse('item:create'),
            self.item_data,
            format="json")

    def test_api_can_create_an_item(self):
        """Test the api has item creation capability."""
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

# class SerializerTestCase(TestCase):
#     """Test suite for the item serializer."""

#     def setUp(self):
#         """Define the test client and other test variables."""
#         self.item_data = {'name': 'Test item'}
#         self.serializer_data = ItemSerializer().data

#     def test_serializer_has_item_field(self):
#         """Test the serializer has an 'item' field."""
#         self.assertEqual('name' in self.serializer_data.fields, True)