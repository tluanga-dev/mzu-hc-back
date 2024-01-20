# views.py

from rest_framework import viewsets
from .models import MedicineDosageDuration
from .serializers import MedicineDosageDurationSerializer

class MedicineDosageDurationViewSet(viewsets.ModelViewSet):
    queryset = MedicineDosageDuration.objects.all()
    serializer_class = MedicineDosageDurationSerializer