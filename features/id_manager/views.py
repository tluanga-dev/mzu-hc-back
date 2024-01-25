from rest_framework import viewsets
from .models import IdManager
from .serializers import IdManagerSerializer

class IdManagerViewSet(viewsets.ModelViewSet):
    queryset = IdManager.objects.all()
    serializer_class = IdManagerSerializer