from unittest import TestCase
from rest_framework.test import APIClient

from features.item.models import ItemCategory, ItemType, UnitOfMeasurement



class BaseTestCase(TestCase):
    def setUp(self):
        
        self.client = APIClient()
        self.item_category = ItemCategory.objects.create(
            name="Test Category",
            abbreviation="TC",
            description="Test Description",
            is_active=True
        )
        self.item_type = ItemType.objects.create(
            name="Test Type",
            abbreviation="TT",
            description="Test Description",
            example="Test Example",
            category=self.item_category,
            is_active=True
        )
        self.unit_of_measurement = UnitOfMeasurement.objects.create(
            name="Test Unit",
            abbreviation="TU",
            description="Test Description",
            example="Test Example",
            is_active=True
        )

    def tearDown(self):
        # Explicitly delete objects if necessary. Usually not required.
        self.unit_of_measurement.delete()
        self.item_type.delete()
        self.item_category.delete()
  