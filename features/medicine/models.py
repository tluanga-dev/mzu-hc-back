from django.db import models

from features.item.models import Item

class MedicineDosage(models.Model):

    quantity_in_one_take = models.IntegerField()
    how_many_times_in_a_day = models.IntegerField()
    name = models.CharField(max_length=255)
    item = models.ForeignKey(Item, related_name='dosages', on_delete=models.CASCADE)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'medicine'

class MedicineDosageDuration(models.Model):
  
    days = models.IntegerField()
    name = models.CharField(max_length=255)
    medicine_dosage = models.ForeignKey(MedicineDosage,  on_delete=models.CASCADE)
    updated_on = models.DateTimeField(auto_now=True)


    class Meta:
        app_label = 'medicine'