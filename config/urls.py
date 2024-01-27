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
from features.id_manager.views import IdManagerViewSet
from features.inventory_transaction.views import IndentInventoryTransactionViewSet

from features.item.item.views import ItemViewSet
from features.item.item_batch.views import ItemBatchViewSet


from features.item.unit_of_measurement.views import UnitOfMeasurementViewSet
from features.item.item_category.views import ItemCategoryViewSet
from features.item.item_type.views import ItemTypeViewSet

# --------Medicine---------
from features.medicine.medicine_dosage.views import MedicineDosageViewSet
from features.medicine.medicine_dosage_duration.views import MedicineDosageDurationViewSet

# --------Transactions---------


# --------Suppliers---------
from features.supplier.views import SupplierViewSet


router = DefaultRouter()
router.register(r'item/units-of-measurement', UnitOfMeasurementViewSet)
router.register(r'item/item_category', ItemCategoryViewSet)
router.register(r'item/item_type', ItemTypeViewSet)

router.register(r'item', ItemViewSet, basename='item')
router.register(r'item/(?P<item_id>[0-9a-f-]+)', ItemBatchViewSet, basename='item')


# --------Medicine---------
router.register(r'medicine/medicine_dosage_duration', MedicineDosageDurationViewSet)
router.register(r'medicine/medicine_dosage', MedicineDosageViewSet)

# --------Suppliers---------
router.register(r'supplier', SupplierViewSet)

#--------Transactions---------
router.register(r'indenttransaction', IndentInventoryTransactionViewSet)

# --------Utilities---------
router.register(r'id_manager', IdManagerViewSet)
urlpatterns = [
    path("admin/", admin.site.urls),
    # --to get all batches of an item
    path('item/<uuid:item_id>/batches', ItemBatchViewSet.as_view({'get': 'item_batches_by_item_id'}), name='item-batches'),
    # --to get a specific batch of an item
    path('item/<uuid:item_id>/batch=<uuid:batch_id>/', ItemBatchViewSet.as_view({'get': 'retrieve_batch'}), name='item-batch-detail'),
    path('', include(router.urls)),
]
