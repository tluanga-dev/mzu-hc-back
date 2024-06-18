import uuid
from django.db import models
from features.base.time_stamped_abstract_class import TimeStampedAbstractModelClass
from features.id_manager.models import IdManager

class ItemPackaging(TimeStampedAbstractModelClass):
    name = models.CharField(max_length=255)
    label = models.CharField(max_length=255, unique=True)
    unit = models.CharField(max_length=255)

    class Meta:
        app_label = 'item'
        indexes = [
            models.Index(fields=['label'], name='packaging_label_idx'),
        ]


class UnitOfMeasurement(TimeStampedAbstractModelClass):  
    name = models.CharField(max_length=255)
    abbreviation = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    example = models.TextField()

    class Meta:
        app_label = 'item'
        indexes = [
            models.Index(fields=['abbreviation'], name='uom_abbreviation_idx'),
        ]


class ItemCategory(TimeStampedAbstractModelClass):
    name = models.CharField(max_length=255, unique=True)
    abbreviation = models.CharField(max_length=4)
    description = models.TextField()
    
    class Meta:
        app_label = 'item'
        indexes = [
            models.Index(fields=['name'], name='itemcategory_name_idx'),
        ]


class ItemType(TimeStampedAbstractModelClass):
    name = models.CharField(max_length=255, unique=True)
    abbreviation = models.CharField(max_length=255)
    description = models.TextField()
    example = models.TextField()
    category = models.ForeignKey(ItemCategory, null=True, on_delete=models.SET_NULL)

    class Meta:
        app_label = 'item'
        indexes = [
            models.Index(fields=['name'], name='itemtype_name_idx'),
        ]

class MedicineDosageUnit(TimeStampedAbstractModelClass):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    example = models.TextField()
    dosage_example = models.TextField()
    class Meta:
        app_label = 'item'
        indexes = [
            models.Index(fields=['name'], name='dosageunit_name_idx'),
        ]


class Item(TimeStampedAbstractModelClass):
    name = models.CharField(max_length=255, unique=True)
    contents = models.TextField(blank=True, null=True)
    item_code = models.CharField(max_length=255, blank=False, null=False, unique=True)
    description = models.TextField()
    type = models.ForeignKey(ItemType, null=True, on_delete=models.SET_NULL)
    unit_of_measurement = models.ForeignKey(UnitOfMeasurement, on_delete=models.CASCADE, related_name='items')
    packaging = models.ForeignKey(ItemPackaging, on_delete=models.CASCADE, related_name='items', null=False, blank=False)
    is_consumable = models.BooleanField(default=False)
    medicine_dosage_unit=models.ManyToManyField(MedicineDosageUnit, related_name='medicine_dosage_unit')
    def save(self, *args, **kwargs):
        if not self.item_code and self.type:
            category_abbreviation = self.type.category.abbreviation
            generated_item_code = IdManager.generateId(category_abbreviation)
            self.item_code = generated_item_code

        super().save(*args, **kwargs)

    class Meta:
        app_label = 'item'
        indexes = [
            models.Index(fields=['name'], name='item_name_idx'),
            models.Index(fields=['item_code'], name='item_code_idx'),
        ]


class ItemBatch(TimeStampedAbstractModelClass):
    batch_id = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    date_of_expiry = models.DateField()
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='item_batches')

 
    class Meta:
        app_label = 'item'
        indexes = [
            models.Index(fields=['batch_id'], name='itembatch_batch_id_idx'),
        ]

