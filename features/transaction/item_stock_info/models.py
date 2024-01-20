from django.db import models

class ItemStockInfo(models.Model):
    quantity = models.IntegerField()
    item = models.OneToOneField('item.Item', on_delete=models.CASCADE)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'item_stock_info'