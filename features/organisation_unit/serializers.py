from rest_framework import serializers
from .models import OrganisationUnit 

class OrganisationUnitSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = OrganisationUnit
        fields = '__all__'