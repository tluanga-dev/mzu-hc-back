
from rest_framework import viewsets

from features.medicine.models import MedicineDosage, MedicineDosageDuration
from features.medicine.serializers import MedicineDosageDurationSerializer, MedicineDosageSerializer

# Create your views here.

class MedicineDosageViewSet(viewsets.ModelViewSet):
    queryset = MedicineDosage.objects.all()
    serializer_class = MedicineDosageSerializer

class MedicineDosageDurationViewSet(viewsets.ModelViewSet):
    queryset = MedicineDosageDuration.objects.all()
    serializer_class = MedicineDosageDurationSerializer