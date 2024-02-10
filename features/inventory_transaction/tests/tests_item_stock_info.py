# from django.utils import timezone
# import datetime
# from features.base.base_test_setup_class import BaseTestCase
# from features.inventory_transaction.models import ItemStockInfo
# from features.item.models import Item, ItemBatch



# class ItemStockInfoModelTest(BaseTestCase):
#     def setUp(self):
#         super().setUp()
#         Item.objects.all().delete()
#         self.item = Item.objects.create(
#             name="Test Item",
#             description="Test Description",
#             type=self.item_type,
#             unit_of_measurement=self.unit_of_measurement,
#             is_active=True
#         )
#         date_of_expiry = timezone.make_aware(datetime.datetime(2022, 12, 31, 23, 59, 59))
#         self.item_batch = ItemBatch.objects.create(batch_id='test', description='test', date_of_expiry=date_of_expiry, item=self.item)

#     def test_read_item_stock_info(self):
      
        
   
#         self.assertEqual(ItemStockInfo.objects.count(), 1)

#         self.assertEqual(ItemBatch.objects.count(), 1)
#         self.assertEqual(self.item_batch.batch_id, 'test')

    