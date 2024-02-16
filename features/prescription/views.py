import datetime
from rest_framework import viewsets

from features.prescription.models import Prescription
from features.prescription.serializers import PrescriptionSerializer

class PrescriptionViewSet(viewsets.ModelViewSet):
    serializer_class = PrescriptionSerializer

    def get_queryset(self):
        queryset = Prescription.objects.all()

        code = self.request.query_params.get('code', None)
        patient_id = self.request.query_params.get('patient_id', None)
        doctor_id = self.request.query_params.get('doctor_id', None)
        date = self.request.query_params.get('date', None)
        date_from = self.request.query_params.get('date_from', None)
        date_to = self.request.query_params.get('date_to', None)
        prescription_dispense_status= self.request.query_params.get('prescription_dispense_status', None)

        if code is not None: 
            queryset = queryset.filter(code=code)
        if patient_id is not None:
            queryset = Prescription.objects.filter(patient__id=patient_id)
            
        if doctor_id is not None:
            queryset =  queryset.filter(doctor_id=doctor_id)
        if date is not None:
            queryset = queryset.filter(prescription_date__exact=date)
        if date_from is not None and date_to is not None:
            queryset = queryset.filter(prescription_date__gte=date_from, prescription_date__lte=date_to)
        if prescription_dispense_status is not None:
            queryset = queryset.filter(prescription_dispense_status=prescription_dispense_status)
     
        return queryset