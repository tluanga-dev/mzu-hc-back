from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

from features.base.base_test_setup_class import BaseTestCase


from django.utils import timezone
import datetime

from features.item.models import Item, ItemBatch
from features.utils.print_json import print_json_string

class ItemBatchModelTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        Item.objects.all().delete()
        self.item_1 = Item.objects.create(
            name="Test Item1",
            description="Test Description1",
            type=self.item_type,
            unit_of_measurement=self.unit_of_measurement,
            is_active=True
        )
        self.item_2 = Item.objects.create(
            name="Test Item2",
            description="Test Description2",
            type=self.item_type,
            unit_of_measurement=self.unit_of_measurement,
            is_active=True
        )
        date_of_expiry = timezone.make_aware(datetime.datetime(2022, 12, 31, 23, 59, 59))
        
        self.item_batch = ItemBatch.objects.create(
            batch_id='test', 
            description='test', 
            date_of_expiry=date_of_expiry, 
            item=self.item_1
        )

        self.item_batch_2 = ItemBatch.objects.create(
            batch_id='test', 
            description='test', 
            date_of_expiry=date_of_expiry, 
            item=self.item_2
        )

    def test_create_item_batch(self):
        self.assertEqual(ItemBatch.objects.count(), 2)
        self.assertEqual(self.item_batch.batch_id, 'test')


class ItemBatchViewSetTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        Item.objects.all().delete()
        self.item = Item.objects.create(
            name="Test Item",
            description="Test Description",
            type=self.item_type,
            unit_of_measurement=self.unit_of_measurement,
            is_active=True
        )
        date_of_expiry = timezone.make_aware(datetime.datetime(2022, 12, 31, 23, 59, 59))
        self.item_batch = ItemBatch.objects.create(batch_id='B1', description='Test Batch', date_of_expiry=date_of_expiry, item=self.item)
       
       
        
    def test_item_batches_by_item_id(self):
        item_batches_url = reverse('item-batches', kwargs={'item_id': str(self.item.id)})
        response = self.client.get(item_batches_url)
        print(response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)    
        self.assertEqual(len(response.data), 1)
       


    def test_retrieve_batch(self):
        item_batch_url = reverse('item-batch-detail', kwargs={'item_id': str(self.item.id), 'batch_id': self.item_batch.batch_id})
        response = self.client.get(item_batch_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['batch_id'], 'B1')
  
       

# class ItemBatchSerializerTest(TestCase):
#     def setUp(self):
#         self.item = Item.objects.create(name='Test Item')
#         self.item_batch = ItemBatch.objects.create(batch_id='test', description='test', date_of_expiry='2022-12-31 23:59:59', item=self.item)

#     def test_serialize_item_batch(self):
#         serializer = ItemBatchSerializer(self.item_batch)
#         self.assertEqual(serializer.data['batch_id'], 'test')

# class ItemBatchViewSetTest(TestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.item = Item.objects.create(name='Test Item')
#         self.item_batch = ItemBatch.objects.create(batch_id='test', description='test', date_of_expiry='2022-12-31 23:59:59', item=self.item)
#         self.url = reverse('itembatch-list')

#     def test_get_all_item_batches(self):
#         response = self.client.get(self.url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     def test_get_single_item_batch(self):
#         response = self.client.get(reverse('itembatch-detail', kwargs={'pk': self.item_batch.pk}))
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     def test_create_item_batch(self):
#         data = {'batch_id': 'new', 'description': 'new', 'date_of_expiry': '2023-12-31 23:59:59', 'item': self.item.id}
#         response = self.client.post(self.url, data)
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)

#     def test_update_item_batch(self):
#         data = {'batch_id': 'updated', 'description': 'updated', 'date_of_expiry': '2023-12-31 23:59:59', 'item': self.item.id}
#         response = self.client.put(reverse('itembatch-detail', kwargs={'pk': self.item_batch.pk}), data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     def test_delete_item_batch(self):
#         response = self.client.delete(reverse('itembatch-detail', kwargs={'pk': self.item_batch.pk}))
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)