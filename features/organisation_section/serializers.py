from rest_framework import serializers
from .models import OrganisationSection 

class OrganisationSectionSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = OrganisationSection
        fields = '__all__'