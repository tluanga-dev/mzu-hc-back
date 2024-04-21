from rest_framework import viewsets, permissions
from django_filters import rest_framework as filters
from features.prescription.models import Prescription
from features.prescription.serializers import PrescriptionSerializer
import logging

logger = logging.getLogger(__name__)

class PrescriptionFilter(filters.FilterSet):
    date_from = filters.DateFilter(field_name="date_and_time", lookup_expr='gte')
    date_to = filters.DateFilter(field_name="date_and_time", lookup_expr='lte')
    date = filters.DateFilter(field_name="date_and_time", lookup_expr='date')
    patient_id = filters.UUIDFilter(field_name="patient__id")  # Filters by the UUID of the patient
    doctor_id = filters.UUIDFilter(field_name="doctor__id")  # Filters by the UUID of the doctor
    patient_mzu_id = filters.CharFilter(field_name="patient__mzu_id")  # Filters by the mzu_id of the patient

    class Meta:
        model = Prescription
        fields = ['code', 'patient_id', 'doctor_id', 'prescription_dispense_status', 'patient_mzu_id']


class PrescriptionViewSet(viewsets.ModelViewSet):
    queryset = Prescription.objects.select_related('patient', 'doctor').prefetch_related('prescribed_item_set')
    serializer_class = PrescriptionSerializer
    permission_classes = [permissions.AllowAny]  # Consider using authenticated permissions
    filter_class = PrescriptionFilter 
    filter_backends = (filters.DjangoFilterBackend,)

    def get_queryset(self):
            """
            Optionally refines the queryset by filtering against query parameters.
            """
            queryset = super().get_queryset()  
            patient_id = self.request.query_params.get('patient_id')
            if patient_id:
                queryset = queryset.filter(patient__id=patient_id)
                print(f"Received patient_id: {patient_id}")# Start with the base queryset

            patient_mzu_id = self.request.query_params.get('patient_mzu_id')
            if(patient_mzu_id):
                queryset = queryset.filter(patient__mzu_id=patient_mzu_id)     

            
            return self.filter_queryset(queryset)  # Use filter_queryset method to apply defined filters



    # def get_queryset(self):
    #     """
    #     Optionally refines the queryset by filtering against query parameters.
    #     """
    #     queryset = super().get_queryset()  # Start with the base queryset
        
    #     # Logging each query parameter received
    #     query_params = self.request.query_params
    #     print(f"Query Parameters: {query_params}")

    #     # For more detailed individual parameter logging:
    #     for param, value in query_params.items():
    #         print("Received filter param: {param} with value: {value}")

    #     # Applying filters
    #     filtered_queryset = self.filter_queryset(queryset)

    #     return filtered_queryset

    
    def handle_exception(self, exc):
        """
        Handle exceptions and possibly perform custom adjustments or logging.
        """
        logger.error(f'Error in processing request: {str(exc)}', exc_info=True)
        return super().handle_exception(exc)

