# models.py

from django.db import models
import uuid

from features.item.item.models import Item



class MedicineDosage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    quantity_in_one_take = models.IntegerField()
    how_many_times_in_a_day = models.IntegerField()
    name = models.CharField(max_length=255)
    item = models.ForeignKey(Item, related_name='dosages', on_delete=models.CASCADE)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'medicine_dosage'