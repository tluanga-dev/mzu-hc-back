

from django.db import models
import uuid


from features.medicine.medicine_dosage.models import MedicineDosage

class MedicineDosageDuration(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    days = models.IntegerField()
    name = models.CharField(max_length=255)
    medicine_dosage = models.ForeignKey(MedicineDosage, related_name='durations', on_delete=models.CASCADE)
    updated_on = models.DateTimeField(auto_now=True)


    class Meta:
        app_label = 'medicine_dosage_duration'