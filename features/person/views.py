from rest_framework import viewsets
import django_filters.rest_framework
from features.person.models import Employee, EmployeeDependent 
from features.person.serializers import  EmployeeDependentSerializer, EmployeeSerializer



# -------Employee

class EmployeeFilter(django_filters.FilterSet):
    mzu_id = django_filters.CharFilter(field_name='employee_id', lookup_expr='icontains')
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    department = django_filters.CharFilter(field_name='department', lookup_expr='icontains')

    class Meta:
        model = Employee
        fields = []

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_class = EmployeeFilter



class EmployeeDependentFilter(django_filters.FilterSet):
    mzu_employee_id = django_filters.CharFilter(field_name='employee__mzu_employee_id', lookup_expr='exact')
    employee_name = django_filters.CharFilter(field_name='employee__name', lookup_expr='icontains')
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    class Meta:
        model = EmployeeDependent
        fields = ['name', 'relation', 'employee__name', 'employee__mzu_employee_id']



# --------Employee Dependent-------
class EmployeeDependentViewSet(viewsets.ModelViewSet):
    queryset = EmployeeDependent.objects.all().select_related('employee')
    serializer_class = EmployeeDependentSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_class = EmployeeDependentFilter

# ---------Student-------------

