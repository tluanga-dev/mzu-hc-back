from rest_framework import viewsets
import django_filters.rest_framework

from features.patient.models import Patient
from features.patient.serializers import PatientSerializer




class PatientFilter(django_filters.FilterSet):
    mzu_id = django_filters.CharFilter(field_name='mzu_id', lookup_expr='icontains')
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    department = django_filters.CharFilter(field_name='department', lookup_expr='icontains')

    class Meta:
        model = Patient
        fields = []

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_class = PatientFilter
