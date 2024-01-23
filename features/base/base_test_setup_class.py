from unittest import TestCase
from rest_framework.test import APIClient
from features.item.item.models import Item

from features.item.item_category.models import ItemCategory
from features.item.item_type.models import ItemType
from features.item.unit_of_measurement.models import UnitOfMeasurement


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
  