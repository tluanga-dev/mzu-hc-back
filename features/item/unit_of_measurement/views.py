from rest_framework import viewsets
from .models import UnitOfMeasurement
from .serializers import UnitOfMeasurementSerializer

class UnitOfMeasurementViewSet(viewsets.ModelViewSet):
    queryset = UnitOfMeasurement.objects.all()
    serializer_class = UnitOfMeasurementSerializer