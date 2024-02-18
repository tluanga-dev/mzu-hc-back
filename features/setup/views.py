from requests import Response
from rest_framework import viewsets

from features.utils.migrate import migrate

class SetupView(viewsets.ViewSet):
    def list(self, request):
        migrate()
        data = {"message": "Hello, world!"}
        return Response(data)