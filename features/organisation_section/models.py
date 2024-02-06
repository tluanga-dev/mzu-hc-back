from django.db import models

from features.base.time_stamped_abstract_class import TimeStampedAbstractModelClass
from features.id_manager.models import IdManager

# Create your models here.
class OrganisationSection(TimeStampedAbstractModelClass):
    name = models.CharField(max_length=100,null=False, blank=False)
    code = models.CharField(max_length=100, unique=True, null=False, blank=False)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
   

    def __str__(self):
        return self.name
   
    
    class Meta:
        app_label = "organisation_section"