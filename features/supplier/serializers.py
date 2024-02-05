from rest_framework import serializers
from .models import Supplier

class SupplierSerializer(serializers.ModelSerializer):
    contact_no = serializers.IntegerField()
    class Meta:
        model = Supplier
        fields = [
            'id', 
            'name', 
            'contact_no', 
            'email', 
            'address', 
            'remarks', 
            'is_active', 
     
        ]