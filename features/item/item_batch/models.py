from django.db import models

from features.item.item.models import Item

class ItemBatch(models.Model):
    batch_id = models.CharField(max_length=255)
    description = models.TextField()
    date_of_expiry = models.DateTimeField()
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'item_batch'