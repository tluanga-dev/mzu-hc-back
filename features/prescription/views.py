from rest_framework import viewsets, permissions
from django_filters import rest_framework as filters
from django.db.models import Q
from django.utils.dateparse import parse_date
from features.prescription.models import Prescription
from features.prescription.serializers import PrescriptionSerializer
import logging

logger = logging.getLogger(__name__)

class PrescriptionFilter(filters.FilterSet):
    date_from = filters.DateFilter(field_name="date_and_time", lookup_expr='gte')
    date_to = filters.DateFilter(field_name="date_and_time", lookup_expr='lte')
    date = filters.DateFilter(field_name="date_and_time", lookup_expr='date')
    
    class Meta:
        model = Prescription
        fields = ['code', 'patient__id', 'doctor__id', 'prescription_dispense_status']

class PrescriptionViewSet(viewsets.ModelViewSet):
    queryset = Prescription.objects.select_related('patient', 'doctor').prefetch_related('prescribed_item_set')
    serializer_class = PrescriptionSerializer
    permission_classes = [permissions.AllowAny]
    filter_class = PrescriptionFilter
    filter_backends = (filters.DjangoFilterBackend,)

    def get_queryset(self):
        """
        Optionally refines the queryset by filtering against query parameters.
        """
        queryset = super().get_queryset()  # Start with the base queryset
        return queryset.filter(self.filterset_class(self.request.GET, queryset=queryset, request=self.request).qs)

    def handle_exception(self, exc):
        """
        Handle exceptions and possibly perform custom adjustments or logging.
        """
        logger.error(f'Error in processing request: {str(exc)}', exc_info=True)
        return super().handle_exception(exc)

# Note: You can add more methods or customize further based on your needs.
