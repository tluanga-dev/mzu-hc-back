# models.py

from django.db import models
from features.item.item_category.models import ItemCategory

class ItemType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    abbreviation = models.CharField(max_length=255)
    description = models.TextField()
    example = models.TextField()
    category = models.ForeignKey(ItemCategory, null=True, on_delete=models.SET_NULL)
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)