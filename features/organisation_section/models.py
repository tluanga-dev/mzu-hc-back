from django.db import models

from features.base.time_stamped_abstract_class import TimeStampedAbstractModelClass

# Create your models here.
class OrganisactionSection(TimeStampedAbstractModelClass):
    name = models.CharField(max_length=100)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
   

    def __str__(self):
        return self.name
    
    class Meta:
        app_label = "organisation_section"