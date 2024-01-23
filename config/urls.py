"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from features.item.item.views import ItemViewSet

from features.item.unit_of_measurement.views import UnitOfMeasurementViewSet
from features.item.item_category.views import ItemCategoryViewSet
from features.item.item_type.views import ItemTypeViewSet

# --------Medicine---------
from features.medicine.medicine_dosage.views import MedicineDosageViewSet
from features.medicine.medicine_dosage_duration.views import MedicineDosageDurationViewSet

# --------Transactions---------
from features.transaction.item_stock_info.views import ItemStockInfoViewSet


router = DefaultRouter()
router.register(r'item/units-of-measurement', UnitOfMeasurementViewSet)
router.register(r'item/item_category', ItemCategoryViewSet)
router.register(r'item/item_type', ItemTypeViewSet)
router.register(r'transaction/item_stock_info', ItemStockInfoViewSet)
router.register(r'item', ItemViewSet)

# --------Medicine---------
router.register(r'medicine/medicine_dosage_duration', MedicineDosageDurationViewSet)
router.register(r'medicine/medicine_dosage', MedicineDosageViewSet)
urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include(router.urls)),
]
