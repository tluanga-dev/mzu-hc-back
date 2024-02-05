# tests.py

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

from features.item.models import ItemCategory, ItemType
from features.item.serializers import ItemTypeSerializer


class ItemTypeModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        ItemCategory.objects.create(name='Test Category', abbreviation='TC', description='Test Description')
        ItemType.objects.create(name='Test Name', abbreviation='TN', description='Test Description', example='Test Example', category=ItemCategory.objects.get(id=1))

    def test_name_label(self):
        itemtype = ItemType.objects.get(id=1)
        field_label = itemtype._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'name')

    def test_abbreviation_label(self):
        itemtype = ItemType.objects.get(id=1)
        field_label = itemtype._meta.get_field('abbreviation').verbose_name
        self.assertEquals(field_label, 'abbreviation')

    # Add more tests as needed

class ItemTypeSerializerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        ItemCategory.objects.create(name='Test Category', abbreviation='TC', description='Test Description')
        ItemType.objects.create(name='Test Name', abbreviation='TN', description='Test Description', example='Test Example', category=ItemCategory.objects.get(id=1))

   

    def test_serializer_data(self):
        itemtype = ItemType.objects.get(id=1)
        serializer = ItemTypeSerializer(itemtype)
        expected_data = {
            'id': 1, 
            'name': 'Test Name', 
            'abbreviation': 'TN', 
            'description': 'Test Description', 
            'example': 'Test Example', 
            'category': 1, 
            'is_active': True, 
            'created_on': itemtype.created_on.isoformat().replace('+00:00', 'Z'),  # Replace this line
            'updated_on': itemtype.updated_on.isoformat().replace('+00:00', 'Z')  # And this line
        }
        self.assertEqual(serializer.data, expected_data)

class ItemTypeViewSetTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        ItemCategory.objects.create(name='Test Category', abbreviation='TC', description='Test Description')
        ItemType.objects.create(name='Test Name', abbreviation='TN', description='Test Description', example='Test Example', category=ItemCategory.objects.get(id=1))

    def test_list_itemtypes(self):
        client = APIClient()
        response = client.get('/item/item_type/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_itemtype(self):
        client = APIClient()
        response = client.get('/item/item_type/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_itemtype(self):
        client = APIClient()
        data = {'name': 'New Name', 'abbreviation': 'NN', 'description': 'New Description', 'example': 'New Example', 'category': 1}
        response = client.post('/item/item_type/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_itemtype(self):
        client = APIClient()
        data = {'name': 'Updated Name', 'abbreviation': 'UN', 'description': 'Updated Description', 'example': 'Updated Example', 'category': 1}
        response = client.put('/item/item_type/1/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_itemtype(self):
        client = APIClient()
        response = client.delete('/item/item_type/1/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    # Add more tests as needed