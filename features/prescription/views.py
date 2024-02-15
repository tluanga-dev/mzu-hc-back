import datetime
from rest_framework import viewsets

from features.prescription.models import Prescription
from features.prescription.serializers import PrescriptionSerializer

class PrescriptionViewSet(viewsets.ModelViewSet):
    serializer_class = PrescriptionSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned prescriptions,
        by filtering against a `code` query parameter in the URL.
        """
        queryset = Prescription.objects.all()
        code = self.kwargs.get('code', None)
        if code is not None:
            queryset = queryset.filter(code=code)

        patient_id = self.kwargs.get('patient_id', None)
        if patient_id is not None:
            queryset = queryset.filter(patient__id=patient_id)

        doctor_id = self.kwargs.get('doctor_id', None)
        if doctor_id is not None:
            queryset = queryset.filter(doctor__id=doctor_id)

        date = self.kwargs.get('date', None)
        if date is not None:
            date = datetime.strptime(date, '%Y-%m-%d').date()
            queryset = queryset.filter(prescription_date__date=date)

        start_date = self.kwargs.get('start_date', None)
        end_date = self.kwargs.get('end_date', None)
        if start_date is not None and end_date is not None:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            queryset = queryset.filter(prescription_date__date__range=(start_date, end_date))
        
        prescription_dispense_status = self.kwargs.get('prescription_dispense_status', None)
        if prescription_dispense_status is not None:
            queryset = queryset.filter(prescription_dispense_status=prescription_dispense_status)
            
        return queryset