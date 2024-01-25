from django.test import TestCase

from features.item.item.models import Item
from .models import IdManager

class IdManagerTest(TestCase):
    def setUp(self):
        self.prefix = 'test'

    def test_generateId(self):
        Item.objects.all().delete()
        # Test the case where the IdManager instance does not exist
        latest_id = IdManager.generateId(self.prefix)
        
        # self.assertEqual(id_manager.latest_id, f'{self.prefix}-AAA0001')
        self.assertEqual(latest_id, f'{self.prefix}-AAA0001')
   


        # Test the case where the IdManager instance exists
        latest_id = IdManager.generateId(self.prefix)
        self.assertEqual(latest_id, f'{self.prefix}-AAA0002')

        # # Test the case where the numeric part reaches '9999'
        id_manager=IdManager.objects.get(prefix=self.prefix)
        id_manager.latest_id = f'{self.prefix}-AAA9999'
        id_manager.save()
        latest_id = IdManager.generateId(self.prefix)
        self.assertEqual(latest_id, f'{self.prefix}-AAB0001')

        # Test the case where the letter part reaches 'ZZZ'
        id_manager.latest_id = f'{self.prefix}-ZZZ9999'
        id_manager.save()
        latest_id = IdManager.generateId(self.prefix)
        self.assertEqual(latest_id, f'{self.prefix}-AAAA0001')