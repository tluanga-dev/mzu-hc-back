# views.py

from rest_framework import viewsets
from .models import MedicineDosage
from .serializers import MedicineDosageSerializer

class MedicineDosageViewSet(viewsets.ModelViewSet):
    queryset = MedicineDosage.objects.all()
    serializer_class = MedicineDosageSerializer