from django.shortcuts import render
from rest_framework import viewsets
from features import organisation_section
from features.organisation_section.serializers import OrganisationSectionSerializer

# Create your views here.
class OrganisationSectionViewSet(viewsets.ModelViewSet):
    queryset = organisation_section.objects.all()
    serializer_class = OrganisationSectionSerializer