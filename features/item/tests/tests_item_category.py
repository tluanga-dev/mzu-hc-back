# # tests.py

# from django.test import TestCase
# from rest_framework.test import APIClient
# from rest_framework import status

# from features.item.models import ItemCategory
# from rest_framework import status
# from rest_framework.test import APIClient


# class ItemCategoryModelTest(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         ItemCategory.objects.create(name='Test Name', abbreviation='TN', description='Test Description')

#     def test_name_label(self):
#         itemcategory = ItemCategory.objects.get(id=1)
#         field_label = itemcategory._meta.get_field('name').verbose_name
#         self.assertEquals(field_label, 'name')

#     def test_abbreviation_label(self):
#         itemcategory = ItemCategory.objects.get(id=1)
#         field_label = itemcategory._meta.get_field('abbreviation').verbose_name
#         self.assertEquals(field_label, 'abbreviation')

#     # Add more tests as needed

# class ItemCategoryViewSetTest(TestCase):
#     @classmethod
#     def setUp(self):
#         self.item_category=ItemCategory.objects.create(
#             name='Test Name', 
#             abbreviation='TN', description='Test Description')

#     def test_list_itemcategories(self):
#         client = APIClient()
#         response = client.get('/item/item_category/')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     def test_retrieve_itemcategory(self):
#         client = APIClient()
#         response = client.get(f'/item/item_category/{self.item_category.id}/')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#         def test_create_itemcategory(self):
#             client = APIClient()
#             data = {'name': 'New Name', 'abbreviation': 'NN', 'description': 'New Description'}
#             response = client.post('/item/item_category/', data)
#             self.assertEqual(response.status_code, status.HTTP_201_CREATED)

#         def test_update_itemcategory(self):
#             client = APIClient()
#             data = {'name': 'Updated Name', 'abbreviation': 'UN', 'description': 'Updated Description'}
#             response = client.put(f'/item/item_category/{self.item_category.id}/', data)
#             print(response)
#             self.assertEqual(response.status_code, status.HTTP_200_OK)

#         def test_delete_itemcategory(self):
#             client = APIClient()
#             response = client.delete('/item/item_category/1/')
#             self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

#     # Add more tests as needed