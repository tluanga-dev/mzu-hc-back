from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework import viewsets, status
from django_filters import rest_framework as filters
from rest_framework.pagination import PageNumberPagination
import logging
from features.medicine.models import MedicineDosage
from features.prescription.models import Prescription, PrescriptionItem
from features.prescription.serializers.create_prescription_serializer import CreatePrescriptionSerializer
from features.prescription.serializers.prescription_detail_serializer import PrescriptionDetailSerializer
from features.prescription.serializers.prescription_serializer import PrescriptionListSerializer, PrescriptionSerializer
from features.prescription.serializers.update_prescription_serializer import UpdatePrescriptionSerializer
from django.db.models import Prefetch

logger = logging.getLogger(__name__)

class PrescriptionFilter(filters.FilterSet):
    date_from = filters.DateFilter(field_name="date_and_time", lookup_expr='gte')
    date_to = filters.DateFilter(field_name="date_and_time", lookup_expr='lte')
    date = filters.DateFilter(field_name="date_and_time", lookup_expr='date')
    patient_id = filters.UUIDFilter(field_name="patient__id")
    patient_mzu_id = filters.CharFilter(field_name="patient__mzu_id")
    patient_type = filters.CharFilter(field_name="patient__patient_type")

    class Meta:
        model = Prescription
        fields = ['code', 'patient_id', 'prescription_dispense_status', 'patient_mzu_id']

class PrescriptionPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class PrescriptionViewSet(viewsets.ModelViewSet):
    queryset = Prescription.objects.all().select_related('patient').prefetch_related(
        Prefetch('prescribed_item_set', queryset=PrescriptionItem.objects.select_related('medicine').prefetch_related(
            Prefetch('dosages', queryset=MedicineDosage.objects.prefetch_related('medicine_dosage_timing_set'))
        ))
    )
    filter_backends = [DjangoFilterBackend]
    filterset_class = PrescriptionFilter
    pagination_class = PrescriptionPagination

    def get_serializer_class(self):
        detail_flag = self.request.query_params.get('detail', '1')
        logger.debug('Action: %s', self.action)
        # example urls-http://localhost:8000/prescription?detail=2
        
        if self.action == 'list':
            if detail_flag == '1':
                return PrescriptionListSerializer
            elif detail_flag == '2':
                return PrescriptionDetailSerializer
        if self.action == 'retrieve':
            return PrescriptionSerializer
        if self.action == 'create':
            return CreatePrescriptionSerializer
        if self.action == 'update':
            return PrescriptionSerializer
        return PrescriptionDetailSerializer

    def retrieve(self, request, pk=None):
        logger.debug('Retrieve action called with pk: %s', pk)
        try:
            instance = Prescription.objects.get(pk=pk)
        except Prescription.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def create(self, request):
        logger.info('Create action called with data: %s', request.data)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            result = serializer.save()
            return Response(result, status=status.HTTP_201_CREATED)
        logger.error('Serializer errors: %s', serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        logger.debug('Update action called with pk: %s', pk)
        try:
            instance = Prescription.objects.get(pk=pk)
        except Prescription.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            result = serializer.save()
            return Response(result, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        try:
            instance = Prescription.objects.get(pk=pk)
        except Prescription.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
