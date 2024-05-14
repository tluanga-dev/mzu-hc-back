from django.shortcuts import render
from rest_framework import viewsets
from features import organisation_unit
from features.organisation_unit.serializers import OrganisationUnitSerializer

# Create your views here.
class OrganisationUnitViewSet(viewsets.ModelViewSet):
    queryset = organisation_unit.objects.all()
    serializer_class = OrganisationUnitSerializer