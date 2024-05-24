# tests.py

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

from features.item.models import ItemCategory, ItemType
from features.item.serializers import ItemTypeSerializer


class ItemTypeModelTest(TestCase):
    @classmethod
    def setUp(self):
        self.item_category= ItemCategory.objects.create(name='Test Category', abbreviation='TC', description='Test Description')
        self.item_type=ItemType.objects.create(name='Test Name', abbreviation='TN', description='Test Description', example='Test Example', category=self.item_category)

    def test_name_label(self):
        itemtype = ItemType.objects.get(id=self.item_type.id)
        field_label = itemtype._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'name')

    def test_abbreviation_label(self):
        itemtype = ItemType.objects.get(id=self.item_type.id)
        field_label = itemtype._meta.get_field('abbreviation').verbose_name
        self.assertEquals(field_label, 'abbreviation')

    # Add more tests as needed

class ItemTypeSerializerTest(TestCase):
    @classmethod
    def setUp(self):
        self.item_category= ItemCategory.objects.create(name='Test Category', abbreviation='TC', description='Test Description')
        self.item_type=ItemType.objects.create(name='Test Name', abbreviation='TN', description='Test Description', example='Test Example', category=self.item_category)

   

    def test_serializer_data(self):
        itemtype = ItemType.objects.get(id=self.item_type.id)
        serializer = ItemTypeSerializer(itemtype)
        expected_data = {
            'id': str(self.item_type.id), 
            'name': 'Test Name', 
            'abbreviation': 'TN', 
            'description': 'Test Description', 
            'example': 'Test Example', 
            'category': self.item_category.id, 
            'is_active': True, 
            'created_at': itemtype.created_at.isoformat().replace('+00:00', 'Z'),  # Replace this line
            'updated_at': itemtype.updated_at.isoformat().replace('+00:00', 'Z')  # And this line
        }
        self.assertEqual(serializer.data, expected_data)

class ItemTypeViewSetTest(TestCase):
    @classmethod
    def setUp(self):
        self.item_category= ItemCategory.objects.create(name='Test Category', abbreviation='TC', description='Test Description')
        self.item_type=ItemType.objects.create(name='Test Name', abbreviation='TN', description='Test Description', example='Test Example', category=self.item_category)

    def test_list_itemtypes(self):
        client = APIClient()
        response = client.get('/item/item_type/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_itemtype(self):
        client = APIClient()
        response = client.get(f'/item/item_type/{self.item_type.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_itemtype(self):
        client = APIClient()
        data = {'name': 'New Name', 'abbreviation': 'NN', 'description': 'New Description', 'example': 'New Example', 'category': str(self.item_category.id )}
        response = client.post('/item/item_type/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_itemtype(self):
        client = APIClient()
        data = {'name': 'Updated Name', 'abbreviation': 'UN', 'description': 'Updated Description', 'example': 'Updated Example', 'category': str(self.item_category.id )}
        url=f'/item/item_type/{str(self.item_type.id)}/'
        response = client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_itemtype(self):
        client = APIClient()
        response = client.delete(f'/item/item_type/{str(self.item_type.id)}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

  