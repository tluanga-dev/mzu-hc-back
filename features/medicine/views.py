
from rest_framework import viewsets

from features.medicine.models import MedicineDosage, MedicineDosageTiming
from features.medicine.serializers import   MedicineDosageSerializer

# Create your views here.

class MedicineDosageViewSet(viewsets.ModelViewSet):
    queryset = MedicineDosage.objects.all()
    serializer_class = MedicineDosageSerializer

