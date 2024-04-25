from rest_framework import viewsets
import django_filters.rest_framework
from features.person.models import Department, Patient, Person, PersonType
from features.person.serializers import DepartmentSerializer, PatientSerializer, PersonSerializer, PersonTypeSerializer

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

class PersonTypeViewSet(viewsets.ModelViewSet):
    queryset = PersonType.objects.all()
    serializer_class = PersonTypeSerializer


class PersonFilter(django_filters.FilterSet):
    mzu_id = django_filters.CharFilter(field_name='mzu_id', lookup_expr='icontains')
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    department = django_filters.CharFilter(field_name='department', lookup_expr='icontains')

    class Meta:
        model = Person
        fields = []

class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_class = PersonFilter

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
  