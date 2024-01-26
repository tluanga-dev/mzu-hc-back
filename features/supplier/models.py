from django.db import models

class Supplier(models.Model):
    name = models.CharField(max_length=255)
    contact_no = models.FloatField()
    email = models.EmailField(max_length=255)
    address = models.TextField()
    remarks = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'supplier'