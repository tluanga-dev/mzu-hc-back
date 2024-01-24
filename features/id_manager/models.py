import uuid
from django.db import models

# Create your models here.
class IdManager(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name=models.CharField(max_length=255)
    description=models.TextField()
    latest_id=models.TextField()
    is_active=models.BooleanField(default=True)

    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'id_manager'
