# myapp/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MedicineViewSet, MedicineDosageViewSet

router = DefaultRouter()
router.register(r'medicines', MedicineViewSet, basename='medicines')
router.register(r'medicine-dosages', MedicineDosageViewSet, basename='medicine-dosages')

urlpatterns = [
    path('medicine/', include(router.urls)),
]
