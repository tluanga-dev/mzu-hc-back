from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from django.utils.dateparse import parse_date
from django.core.exceptions import ValidationError

from features.inventory_transaction.dispense_transaction.models import DispenseInventoryTransaction
from features.inventory_transaction.dispense_transaction.serializers import DispenseInventoryTransactionSerializer
from features.prescription.models import Prescription
from features.patient.models import Patient
from features.user.models import CustomUser

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class DispenseInventoryTransactionViewSet(viewsets.ModelViewSet):
    queryset = DispenseInventoryTransaction.objects.all()
    serializer_class = DispenseInventoryTransactionSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        """
        Optionally restricts the returned dispense inventory transactions by filtering against
        query parameters in the URL.
        """
        queryset = DispenseInventoryTransaction.objects.all().select_related(
            'prescription__patient', 'prescription__doctor'
        )
        
        # Extract and validate query parameters
        prescription_code = self.request.query_params.get('prescription')
        status = self.request.query_params.get('status')
        patient_code = self.request.query_params.get('patient')
        doctor_code = self.request.query_params.get('doctor')
        dispense_date = self.request.query_params.get('dispense_date')
        dispense_date_from = self.request.query_params.get('dispense_date_from')
        dispense_date_to = self.request.query_params.get('dispense_date_to')

        # Filter by prescription code
        if prescription_code:
            queryset = queryset.filter(prescription__code=prescription_code)

        # Filter by patient code
        if patient_code:
            queryset = queryset.filter(prescription__patient__code=patient_code)

        # Filter by doctor code
        if doctor_code:
            queryset = queryset.filter(prescription__doctor__code=doctor_code)

        # Filter by status
        if status:
            queryset = queryset.filter(status=status)

        # Filter by exact dispense date
        if dispense_date:
            try:
                dispense_date_parsed = parse_date(dispense_date)
                if dispense_date_parsed:
                    queryset = queryset.filter(dispense_date__date=dispense_date_parsed)
            except ValidationError:
                pass  # Handle invalid date format gracefully

        # Filter by dispense date range
        if dispense_date_from and dispense_date_to:
            try:
                dispense_date_from_parsed = parse_date(dispense_date_from)
                dispense_date_to_parsed = parse_date(dispense_date_to)
                if dispense_date_from_parsed and dispense_date_to_parsed:
                    queryset = queryset.filter(dispense_date__date__range=[dispense_date_from_parsed, dispense_date_to_parsed])
            except ValidationError:
                pass  # Handle invalid date range format gracefully

        return queryset

    def list(self, request, *args, **kwargs):
        """
        Return a paginated list of dispense inventory transactions.
        """
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        """
        Return a single dispense inventory transaction instance.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
