from datetime import datetime
import uuid
from django.db import models

from features.id_manager.generate_id import generate_next_id

# Create your models here.
class IdManager(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    prefix=models.CharField(max_length=255, unique=True)
    latest_id=models.TextField()
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    @classmethod
    def generateId(cls, prefix):
       
        id_manager, created = cls.objects.get_or_create(prefix=prefix, defaults={'latest_id': f"{prefix}-AAA0001"})
        if not created:
            # step 1, get the latest id
            latest_id = id_manager.latest_id
         
            print('latest_id', latest_id)
            # step 2, generate the next id
            next_id = generate_next_id(latest_id)
            print('next_id', next_id)
            # step 3, update the latest id
            id_manager.latest_id = next_id
            # step 4, update  updated_on
            id_manager.updated_on = datetime.now()
            id_manager.save()  
            
            
            
 
            return id_manager.latest_id 
        else:
            return id_manager.latest_id
            
        
    
    