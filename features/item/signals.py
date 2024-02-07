from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ItemStockInfo, Item

@receiver(post_save, sender=Item)
def post_save_item(sender, instance, created, **kwargs):
    if created:
        ItemStockInfo.objects.create(
            item=instance,
            quantity=0, 
        
        )  
    else:
        instance.item_stock_info.save()