from django.db import models

# Create your models here.
class Setup(models.Model):
    is_data_migrated = models.BooleanField(default=False)
    class Meta:
        app_label = "setup"
