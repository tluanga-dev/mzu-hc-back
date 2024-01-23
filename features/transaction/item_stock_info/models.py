from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save

from features.item.item.models import Item

class ItemStockInfo(models.Model):
    quantity = models.IntegerField()
    item = models.OneToOneField('item.Item', on_delete=models.CASCADE)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'item_stock_info'


@receiver(post_save, sender=Item)
def create_item_stock_info(sender, instance, created, **kwargs):
    if created:
        item_stock_info=ItemStockInfo.objects.create(item=instance,quantity=0)
     
    else:
        ItemStockInfo.objects.get_or_create(item=instance)