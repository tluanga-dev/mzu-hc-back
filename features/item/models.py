import uuid
from django.db import models
from features.base.time_stamped_abstract_class import TimeStampedAbstractModelClass
from features.id_manager.models import IdManager


class UnitOfMeasurement(models.Model):
    name = models.CharField(max_length=255)
    abbreviation = models.CharField(max_length=255)
    description = models.TextField()
    example = models.TextField()
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

class ItemCategory(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    abbreviation = models.CharField(max_length=4)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    class Meta:
        app_label = 'item'

class ItemType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    abbreviation = models.CharField(max_length=255)
    description = models.TextField()
    example = models.TextField()
    category = models.ForeignKey(ItemCategory, null=True, on_delete=models.SET_NULL)
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)


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
            generated_item_code = IdManager.generateId(category_abbreviation)
            # print(generated_item_code)
            self.item_code = generated_item_code

        super().save(*args, **kwargs)

    class Meta:
        app_label = 'item'

class ItemBatch(models.Model):
    batch_id = models.CharField(max_length=255)
    description = models.TextField()
    date_of_expiry = models.DateField()
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='item_batches')
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
      

        super().save(*args, **kwargs)

    class Meta:
        app_label = 'item'


