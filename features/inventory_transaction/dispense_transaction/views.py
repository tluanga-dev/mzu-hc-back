from features.inventory_transaction.dispense_transaction.models import DispenseInventoryTransaction
from features.inventory_transaction.dispense_transaction.serializers import DispenseInventoryTransactionSerializer
from rest_framework import viewsets



class DispenseInventoryTransactionViewSet(viewsets.ModelViewSet):
    queryset = DispenseInventoryTransaction.objects.all()
    serializer_class = DispenseInventoryTransactionSerializer

    def get_queryset(self):
        queryset = DispenseInventoryTransaction.objects.all()
        prescription = self.request.query_params.get('prescription', None)
        status = self.request.query_params.get('status', None)  
        patient = self.request.query_params.get('patient', None)
        doctor= self.request.query_params.get('doctor', None)
        dispense_date = self.request.query_params.get('dispense_date', None)
        dispense_date_from = self.request.query_params.get('dispense_date_from', None)
        dispense_date_to = self.request.query_params.get('dispense_date_to', None)

        if prescription is not None:
            prescription_obj = prescription.objects.get(code=prescription)
            if prescription_obj is not None:
                queryset = queryset.filter(prescription=prescription_obj)

        if patient is not None:
            patient_obj = patient.objects.get(code=patient)
            if patient_obj is not None:
                queryset = queryset.filter(prescription__patient=patient_obj)

        if doctor is not None:
            doctor_obj = patient.objects.get(code=doctor)
            if doctor_obj is not None:
                queryset = queryset.filter(prescription__doctor=doctor_obj)

        if status is not None:
            queryset = queryset.filter(status=status)
      
        
        if dispense_date is not None:
            queryset = queryset.filter(dispense_date__exact=dispense_date)

        if dispense_date_from is not None and dispense_date_to is not None:
            
            queryset = queryset.filter(dispense_date__gte=dispense_date_from, dispense_date__lte=dispense_date_to)

        return queryset
    
