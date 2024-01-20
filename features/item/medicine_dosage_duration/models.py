# models.py

from django.db import models
import uuid

class MedicineDosageDuration(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    days = models.IntegerField()
    name = models.CharField(max_length=255)
    updated_on = models.DateTimeField(auto_now=True)