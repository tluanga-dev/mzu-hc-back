from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
import django_filters.rest_framework
from django_filters import rest_framework as filters
from features.patient.models import Patient
from features.patient.serializers import PatientSerializer

class PatientFilter(filters.FilterSet):
    """Filter set for Patient model."""
    mzu_id = filters.CharFilter(field_name='mzu_hc_id', lookup_expr='icontains')
    patient_type = filters.CharFilter(field_name='patient_type', lookup_expr='icontains')
    illness = filters.CharFilter(field_name='illness', lookup_expr='icontains')
    allergy = filters.CharFilter(field_name='allergy', lookup_expr='icontains')

    class Meta:
        model = Patient
        fields = ['mzu_hc_id', 'patient_type', 'illness', 'allergy']

class StandardResultsSetPagination(PageNumberPagination):
    """Standard pagination settings for the API results."""
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class PatientViewSet(viewsets.ModelViewSet):
    """View set for Patient model."""
    queryset = Patient.objects.all().select_related('employee', 'student', 'employee_dependent', 'mzu_outsider_patient')
    serializer_class = PatientSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_class = PatientFilter
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        """
        Optionally restricts the returned patients to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = self.queryset
        mzu_hc_id = self.request.query_params.get('mzu_hc_id', None)
        if mzu_hc_id is not None:
            queryset = queryset.filter(mzu_hc_id__icontains=mzu_hc_id)
        return queryset
