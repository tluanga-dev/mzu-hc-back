
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework import viewsets, status
from django_filters import rest_framework as filters
from features.prescription.models import Prescription
from rest_framework.pagination import PageNumberPagination
import logging
from rest_framework.decorators import action
from features.prescription.serializers.create_prescription_serializer import CreatePrescriptionSerializer
from features.prescription.serializers.prescription_serializer import PrescriptionDetailSerializer, PrescriptionListSerializer
from features.prescription.serializers.update_prescription_serializer import UpdatePrescriptionSerializer



logger = logging.getLogger(__name__)

class PrescriptionFilter(filters.FilterSet):
    date_from = filters.DateFilter(field_name="date_and_time", lookup_expr='gte')
    date_to = filters.DateFilter(field_name="date_and_time", lookup_expr='lte')
    date = filters.DateFilter(field_name="date_and_time", lookup_expr='date')
    patient_id = filters.UUIDFilter(field_name="patient__id")  # Filters by the UUID of the patient
    # doctor_id = filters.UUIDFilter(field_name="doctor__id")  # Filters by the UUID of the doctor
    patient_mzu_id = filters.CharFilter(field_name="patient__mzu_id")
    patient_type = filters.CharFilter(field_name="patient__patient_type")  # Filters by the mzu_id of the patient

    class Meta:
        model = Prescription
        fields = ['code', 'patient_id', 'prescription_dispense_status', 'patient_mzu_id']

class PrescriptionPagination(PageNumberPagination):
    page_size = 10  # Default page size
    page_size_query_param = 'page_size'
    max_page_size = 100

class PrescriptionViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides the standard actions
    """
    queryset = Prescription.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = PrescriptionFilter
    pagination_class = PrescriptionPagination

    def get_serializer_class(self):
        if self.action == 'list':
            return PrescriptionListSerializer
        if self.action == 'retrieve':
            return PrescriptionDetailSerializer
        if self.action == 'create':
            return CreatePrescriptionSerializer
        if self.action == 'update':
            return UpdatePrescriptionSerializer
        return PrescriptionDetailSerializer

    def create(self, request):
        """
        Handle the creation of a prescription and patient.
        """
        serializer = self.get_serializer(data=request.data)
      
        if serializer.is_valid():
            result = serializer.save()
            return Response(result, status=status.HTTP_201_CREATED)
       
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  
    def update(self, request, pk=None):
        """
        Handle updating of an existing prescription.
        """
        try:
            instance = Prescription.objects.get(pk=pk)
        except Prescription.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            result = serializer.save()
            return Response(result, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """
        Retrieve a single prescription.
        """
        try:
            instance = Prescription.objects.get(pk=pk)
        except Prescription.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def list(self, request):
        """
        List all prescriptions.
        """
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def destroy(self, request, pk=None):
        """
        Delete a single prescription.
        """
        try:
            instance = Prescription.objects.get(pk=pk)
        except Prescription.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
