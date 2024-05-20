from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from django.utils.dateparse import parse_date

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
        queryset = DispenseInventoryTransaction.objects.all().select_related(
            'prescription__patient', 'prescription__doctor'
        )
        
        prescription_code = self.request.query_params.get('prescription', None)
        status = self.request.query_params.get('status', None)
        patient_code = self.request.query_params.get('patient', None)
        doctor_code = self.request.query_params.get('doctor', None)
        dispense_date = self.request.query_params.get('dispense_date', None)
        dispense_date_from = self.request.query_params.get('dispense_date_from', None)
        dispense_date_to = self.request.query_params.get('dispense_date_to', None)

        if prescription_code:
            prescription_obj = get_object_or_404(Prescription, code=prescription_code)
            queryset = queryset.filter(prescription=prescription_obj)

        if patient_code:
            patient_obj = get_object_or_404(Patient, code=patient_code)
            queryset = queryset.filter(prescription__patient=patient_obj)

        # if doctor_code:
        #     doctor_obj = get_object_or_404(CustomUser, code=doctor_code)
        #     queryset = queryset.filter(prescription__doctor=doctor_obj)

        if status:
            queryset = queryset.filter(status=status)

        if dispense_date:
            dispense_date_parsed = parse_date(dispense_date)
            if dispense_date_parsed:
                queryset = queryset.filter(dispense_date__exact=dispense_date_parsed)

        if dispense_date_from and dispense_date_to:
            dispense_date_from_parsed = parse_date(dispense_date_from)
            dispense_date_to_parsed = parse_date(dispense_date_to)
            if dispense_date_from_parsed and dispense_date_to_parsed:
                queryset = queryset.filter(dispense_date__gte=dispense_date_from_parsed,
                                           dispense_date__lte=dispense_date_to_parsed)

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
