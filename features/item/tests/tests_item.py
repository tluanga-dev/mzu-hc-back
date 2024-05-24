# tests.py

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from features.base.base_test_setup_class import BaseTestCase
from features.id_manager.models import IdManager
from features.item.models import Item
from features.item.serializers import ItemSerializer



class ItemModelTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
    
    def test_create_item(self):
        Item.objects.all().delete()
        IdManager.objects.all().delete()
        item = Item.objects.create(
            name='Test Item',
            description='This is a test item',
            type=self.item_type,
            unit_of_measurement=self.unit_of_measurement
        )
        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(item.name, 'Test Item')
        self.assertEqual(item.description, 'This is a test item')
        self.assertEqual(item.type, self.item_type)
        self.assertEqual(item.unit_of_measurement, self.unit_of_measurement)
        self.assertTrue(item.is_active)

    def test_item_code_generation(self):
        
        item = Item.objects.create(
            name='Test Item',
            description='This is a test item',
            type=self.item_type,
            unit_of_measurement=self.unit_of_measurement
        )
        alpha_part = item.item_code.rstrip('0123456789')
        num_part = item.item_code[len(alpha_part):]

        # Increment the numeric part
        new_num = str(int(num_part) + 1).zfill(len(num_part))

        # Return the incremented string
        new_code= alpha_part + new_num
        self.assertIsNotNone(item.item_code)
        self.assertEqual(new_code, IdManager.generateId(self.item_type.category.abbreviation))

    def test_item_update(self):
        item = Item.objects.create(
            name='Test Item',
            description='This is a test item',
            type=self.item_type,
            unit_of_measurement=self.unit_of_measurement
        )
        item.name = 'Updated Item'
        item.save()
        self.assertEqual(Item.objects.get(id=item.id).name, 'Updated Item')

    def test_item_deletion(self):
        item = Item.objects.create(
            name='Test Item',
            description='This is a test item',
            type=self.item_type,
            unit_of_measurement=self.unit_of_measurement
        )
        item_id = item.id
        item.delete()
        self.assertFalse(Item.objects.filter(id=item_id).exists())


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
        self.assertCountEqual(data.keys(), ['id', 'name', 'description', 'type', 'is_active', 'created_at', 'updated_at'])

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
