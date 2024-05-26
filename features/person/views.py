from rest_framework import viewsets
import django_filters.rest_framework
from features.person.models import Employee, EmployeeDependent,  MZUOutsider, Student 
from features.person.serializers import  EmployeeDependentSerializer, EmployeeSerializer,  MZUOutsiderSerializer, StudentSerializer
from rest_framework.pagination import PageNumberPagination

class StandardResultsSetPagination(PageNumberPagination):
    """Standard pagination settings for the API results."""
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

# -------Employee

class EmployeeFilter(django_filters.FilterSet):
    mzu_id = django_filters.CharFilter(field_name='employee_id', lookup_expr='icontains')
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    organisation_unit = django_filters.CharFilter(field_name='organisation_unit', lookup_expr='icontains')
    employee_type = django_filters.CharFilter(field_name='employee_type', lookup_expr='iexact')

    class Meta:
        model = Employee
        fields = ['mzu_id', 'name', 'employee_type']

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_class = EmployeeFilter
    pagination_class = StandardResultsSetPagination


# ---------Employee Dependent-------------

class EmployeeDependentFilter(django_filters.FilterSet):
    mzu_employee_id = django_filters.CharFilter(field_name='employee__mzu_employee_id', lookup_expr='exact')
    employee_name = django_filters.CharFilter(field_name='employee__name', lookup_expr='icontains')
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
   
    class Meta:
        model = EmployeeDependent
        fields = ['name', 'relation', 'employee__name', 'employee__mzu_employee_id']




class EmployeeDependentViewSet(viewsets.ModelViewSet):
    queryset = EmployeeDependent.objects.all().select_related('employee')
    serializer_class = EmployeeDependentSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_class = EmployeeDependentFilter
    pagination_class = StandardResultsSetPagination
# ---------Student-------------
class StudentFilter(django_filters.FilterSet):
    mzu_student_id = django_filters.CharFilter(field_name='mzu_student_id', lookup_expr='exact')
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    class Meta:
        model = Student
        fields = ['name', 'mzu_student_id']



# --------Employee Dependent-------
class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_class = StudentFilter
    pagination_class = StandardResultsSetPagination

# ---------MZU OUTSIDER-------------
class MZUOutsiderFilter(django_filters.FilterSet):
    # mzu_student_id = django_filters.CharFilter(field_name='mzu_student_id', lookup_expr='exact')
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    class Meta:
        model = MZUOutsider
        fields = ['name']



class MZUOutsiderViewSet(viewsets.ModelViewSet):
    queryset = MZUOutsider.objects.all()
    serializer_class = MZUOutsiderSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_class = MZUOutsiderFilter
    pagination_class = StandardResultsSetPagination