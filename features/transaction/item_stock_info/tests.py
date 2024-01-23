from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from features.base.base_test_setup_class import BaseTestCase
from features.transaction.item_stock_info.models import ItemStockInfo
from features.item.item.models import Item
from features.transaction.item_stock_info.serializers import ItemStockInfoSerializer  # assuming this is the correct import for Item

class ItemStockInfoTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.item = Item.objects.create(
            name="Test Item",
            description="Test Description",
            type=self.item_type,
            unit_of_measurement=self.unit_of_measurement,
            is_active=True
        )
        self.item_stock_info = ItemStockInfo.objects.create(quantity=10, item=self.item)
        self.serializer = ItemStockInfoSerializer(instance=self.item_stock_info)
        self.url = reverse('itemstockinfo-list')  # replace 'itemstockinfo-list' with the actual name of the URL pattern

    # -------Test the model------
    def test_item_stock_info_creation(self):
        self.assertIsInstance(self.item_stock_info, ItemStockInfo)

    def test_item_stock_info_fields(self):
        self.assertEqual(self.item_stock_info.quantity, 10)
        self.assertEqual(self.item_stock_info.item, self.item)

    def test_updated_on_auto_now(self):
        old_updated_on = self.item_stock_info.updated_on
        self.item_stock_info.quantity = 20
        self.item_stock_info.save()
        self.assertNotEqual(self.item_stock_info.updated_on, old_updated_on)


    # -------Test the serializer------
    
    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertCountEqual(data.keys(), ['id', 'quantity', 'item', 'updated_on'])

    def test_quantity_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['quantity'], self.item_stock_info.quantity)

    def test_item_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['item'], self.item_stock_info.item.id)  # assuming item is serialized as its id

    # -------Test the viewset------
    def test_get_all_item_stock_infos(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_single_item_stock_info(self):
        url = reverse('itemstockinfo-detail', kwargs={'pk': self.item_stock_info.pk})  # replace 'itemstockinfo-detail' with the actual name of the URL pattern
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_item_stock_info(self):
        ItemStockInfo.objects.all().delete()
        data = {
            'quantity': 20,
            'item': self.item.id,
        }
        response = self.client.post(self.url, data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_item_stock_info(self):
        url = reverse('itemstockinfo-detail', kwargs={'pk': self.item_stock_info.pk})  # replace 'itemstockinfo-detail' with the actual name of the URL pattern
        data = {
            'quantity': 30,
            'item': self.item.id,
      
        }
        response = self.client.put(url, data)
        print('---response',response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_item_stock_info(self):
        url = reverse('itemstockinfo-detail', kwargs={'pk': self.item_stock_info.pk})  # replace 'itemstockinfo-detail' with the actual name of the URL pattern
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)