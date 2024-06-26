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
from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from features.id_manager.views import IdManagerViewSet
from features.inventory_transaction.dispense_transaction.views import DispenseInventoryTransactionViewSet
from features.inventory_transaction.indent_transaction.views import IndentInventoryTransactionViewSet
from features.inventory_transaction.inventory_transaction.views import ItemTransactionsView
from features.inventory_transaction.issue_transaction.views import IssueItemInventoryTransactionViewSet
from features.item.views import ItemBatchViewSet, ItemCategoryViewSet, ItemTypeViewSet, ItemViewSet, UnitOfMeasurementViewSet
from features.medicine.views import MedicineDosageDurationViewSet, MedicineDosageViewSet
from features.person.views import DepartmentViewSet, PersonTypeViewSet, PersonViewSet
from features.prescription.views import PrescriptionViewSet
from features.setup.views import SetupView




# --------Suppliers---------
from features.supplier.views import SupplierViewSet


router = DefaultRouter()
router.register(r'item/units-of-measurement', UnitOfMeasurementViewSet,basename='unit-of-measurement')
router.register(r'item/item_category', ItemCategoryViewSet)
router.register(r'item/item_type', ItemTypeViewSet)

router.register(r'item', ItemViewSet, basename='item')




# --------Medicine---------
router.register(r'medicine/medicine_dosage_duration', MedicineDosageDurationViewSet)
router.register(r'medicine/medicine_dosage', MedicineDosageViewSet)

# --------Suppliers---------
router.register(r'supplier', SupplierViewSet)

#--------Transactions---------
router.register(r'transaction/indent', IndentInventoryTransactionViewSet, basename='indent-inventory-transactions')
router.register(r'transaction/issue_item', IssueItemInventoryTransactionViewSet, basename='issue-item-inventory-transactions')
router.register(r'transaction/dispense', DispenseInventoryTransactionViewSet, basename='dispense-inventory-transactions')

# -------Person-----
router.register(r'department', DepartmentViewSet, basename='department')
router.register(r'person_type', PersonTypeViewSet,basename='person-type')
router.register(r'person', PersonViewSet,basename='person')


# --------Prescription---------
router.register(r'prescriptions', PrescriptionViewSet, basename='prescription')

router.register(r'setup', SetupView, basename='setup')

# --------Utilities---------
router.register(r'id_manager', IdManagerViewSet)
urlpatterns = [
    path("admin/", admin.site.urls),
    # --to get all batches of an item
    # path('item/<int:item_id>/batches', ItemBatchViewSet.as_view({'get': 'item_batches_by_item_id'}), name='item-batches'),
    # # --to get a specific batch of an item
    # re_path(r'^item/(?P<item_id>[0-9a-f-]+)/batches/$', ItemBatchViewSet.as_view({'get': 'item_batches_by_item_id'}), name='item-batches'),
    re_path(r'^item/(?P<item_id>[0-9a-f-]+)/batches/$', ItemBatchViewSet.as_view({'get': 'item_batches_by_item_id', 'post': 'create'}), name='item-batches'),

    path('item/<uuid:item_id>/<str:batch_id>/', ItemBatchViewSet.as_view({'get': 'retrieve_batch'}), name='item-batch-detail'),
    
    path('transactions/<str:pk>/', ItemTransactionsView.as_view({'get':'retrieve'}), name='item-transactions-detail'),
    
    re_path(r'^item/(?P<item_id>[0-9a-f-]+)/batches/$', ItemBatchViewSet.as_view({'get': 'item_batches_by_item_id'}), name='item-batches'),
   
  
    path('', include(router.urls)),
]
