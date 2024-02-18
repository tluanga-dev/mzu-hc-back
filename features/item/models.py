import uuid
from django.db import models
from features.base.time_stamped_abstract_class import TimeStampedAbstractModelClass
from features.id_manager.models import IdManager


class UnitOfMeasurement(TimeStampedAbstractModelClass):  
    name = models.CharField(max_length=255)
    abbreviation = models.CharField(max_length=255)
    description = models.TextField()
    example = models.TextField()

    class Meta:
        app_label = 'item'


class ItemCategory(TimeStampedAbstractModelClass):
    name = models.CharField(max_length=255)
    abbreviation = models.CharField(max_length=4)
    description = models.TextField()
    
    class Meta:
        app_label = 'item'

class ItemType(TimeStampedAbstractModelClass):
    name = models.CharField(max_length=255)
    abbreviation = models.CharField(max_length=255)
    description = models.TextField()
    example = models.TextField()
    category = models.ForeignKey(ItemCategory, null=True, on_delete=models.SET_NULL)

    class Meta:
        app_label = 'item'



class Item(TimeStampedAbstractModelClass):
    name = models.CharField(max_length=255)
    item_code = models.CharField(max_length=255, blank=False, null=False, unique=True)
    description = models.TextField()
    type = models.ForeignKey(ItemType, null=True, on_delete=models.SET_NULL)
    unit_of_measurement = models.ForeignKey(UnitOfMeasurement, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.item_code and self.type:
            category_abbreviation = self.type.category.abbreviation
            generated_item_code = IdManager.generateId(category_abbreviation)
            # print(generated_item_code)
            self.item_code = generated_item_code

        super().save(*args, **kwargs)

    class Meta:
        app_label = 'item'

class ItemBatch(TimeStampedAbstractModelClass):
    batch_id = models.CharField(max_length=255)
    description = models.TextField()
    date_of_expiry = models.DateField()
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='item_batches')

    def save(self, *args, **kwargs):
      

        super().save(*args, **kwargs)

    class Meta:
        app_label = 'item'


