from rest_framework import serializers
from .models import OrganisactionSection

class OrganisationSectionSerializer(serializers.ModelSerializer):
    contact_no = serializers.IntegerField()
    class Meta:
        model = OrganisactionSection
        fields = '__all__'