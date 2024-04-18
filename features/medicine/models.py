import uuid
from django.db import models
from features.base.time_stamped_abstract_class import TimeStampedAbstractModelClass

from features.item.models import Item

class MedicineDosage(TimeStampedAbstractModelClass):
    quantity_in_one_take = models.IntegerField()
    how_many_times_in_a_day = models.IntegerField()
    name = models.CharField(max_length=255)
    item = models.ForeignKey(Item, related_name='dosages', on_delete=models.CASCADE)


    class Meta:
        app_label = 'medicine'

class MedicineDosageDuration(TimeStampedAbstractModelClass):
    days = models.IntegerField()
    name = models.CharField(max_length=255)
    medicine_dosage = models.ForeignKey(MedicineDosage,  on_delete=models.CASCADE)



    class Meta:
        app_label = 'medicine'