import uuid
from django.db import models
from features.id_manager.models import IdManager

from features.item.item_type.models import ItemType
from features.item.unit_of_measurement.models import UnitOfMeasurement



class Item(models.Model):
    """
    Represents an item in the system.

    Attributes:
        id (UUIDField): The unique identifier for the item.
        name (CharField): The name of the item.
        description (TextField): The description of the item.
        type (ForeignKey): The type of the item.
        unit_of_measurement (ForeignKey): The unit of measurement for the item.
        is_active (BooleanField): Indicates whether the item is active or not.
        created_on (DateTimeField): The date and time when the item was created.
        updated_on (DateTimeField): The date and time when the item was last updated.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    item_code = models.CharField(max_length=255, blank=False, null=False, unique=True)
    description = models.TextField()
    type = models.ForeignKey(ItemType, null=True, on_delete=models.SET_NULL)
    unit_of_measurement = models.ForeignKey(UnitOfMeasurement, on_delete=models.CASCADE)

    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)


    def save(self, *args, **kwargs):
        if not self.item_code and self.type:
            category_abbreviation = self.type.category.abbreviation
            # self.item_code = IdManager.generateId(category_abbreviation)

        super().save(*args, **kwargs)

    class Meta:
        app_label = 'item'

    