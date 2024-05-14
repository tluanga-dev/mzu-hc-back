import uuid
from django.db import models

from features.base.time_stamped_abstract_class import TimeStampedAbstractModelClass
from features.id_manager.models import IdManager

# -----Department-----
class OrganisationUnit(TimeStampedAbstractModelClass):
    name = models.CharField(max_length=100,null=False, blank=False)
    abbreviation = models.CharField(max_length=100, unique=True, null=False, blank=False)
    description = models.TextField()
  
    def __str__(self):
        return self.name
   
    
    class Meta:
        app_label = "organisation_unit"