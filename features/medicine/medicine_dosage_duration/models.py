

from django.db import models
import uuid

from features.item.item.models import Item

class MedicineDosageDuration(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    days = models.IntegerField()
    name = models.CharField(max_length=255)
    item = models.ForeignKey(Item, null=True, on_delete=models.SET_NULL)
    updated_on = models.DateTimeField(auto_now=True)


    class Meta:
        app_label = 'medicine_dosage_duration'