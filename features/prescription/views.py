import datetime
from rest_framework import viewsets

from features.prescription.models import Prescription
from features.prescription.serializers import PrescriptionSerializer
from features.utils.convert_date import convert_date_format
from features.prescription.models import Prescription
from features.utils.convert_date import convert_date_format

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
            date = convert_date_format(date)
            queryset = queryset.filter(date_and_time__date=date)

        if date_from is not None and date_to is not None:
            converted_date_from=convert_date_format(date_from)
            print(f"converted_date_from: {converted_date_from}")
            converted_date_to=convert_date_format(date_to)
            print(f"converted_date_to: {converted_date_to}")
            # comparting the date part only
            queryset = queryset.filter(
                date_and_time__date__gte=converted_date_from, date_and_time__date__lte=converted_date_to)
        
       
        if prescription_dispense_status is not None:
            queryset = queryset.filter(prescription_dispense_status=prescription_dispense_status)
     
        return queryset