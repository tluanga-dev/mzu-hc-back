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
from features.inventory_transaction.dispense_transaction.views import DispenseInventoryTransactionViewSet, ItemInformationForDispenseTransactionViewSet
from features.inventory_transaction.indent_transaction.views import IndentInventoryTransactionViewSet
from features.inventory_transaction.inventory_transaction.views import ItemTransactionsView
from features.inventory_transaction.issue_transaction.views import IssueItemInventoryTransactionViewSet
from features.item.views import ItemBatchViewSet, ItemCategoryViewSet, ItemTypeViewSet, ItemViewSet, ItemWithStockInfoViewSet, UnitOfMeasurementViewSet
from features.medicine.views import  MedicineDosageViewSet
from features.person.views import DepartmentViewSet, PersonTypeViewSet, PersonViewSet
from features.prescription.views import PrescriptionViewSet, PrescriptionViewSetForDispense
from features.setup.views import SetupView




# --------Suppliers---------
from features.supplier.views import SupplierViewSet


router = DefaultRouter()
router.register(r'item/units-of-measurement', UnitOfMeasurementViewSet,basename='unit-of-measurement')
router.register(r'item/item_category', ItemCategoryViewSet)
router.register(r'item/item_type', ItemTypeViewSet)
router.register(r'item_with_stock_info', ItemWithStockInfoViewSet)

router.register(r'item', ItemViewSet, basename='item')






# --------Medicine---------
router.register(r'medicine/medicine_dosage', MedicineDosageViewSet)

# --------Suppliers---------
router.register(r'supplier', SupplierViewSet)

#--------Transactions---------
router.register(r'transaction/indent', IndentInventoryTransactionViewSet, basename='indent-inventory-transactions')
router.register(r'transaction/issue_item', IssueItemInventoryTransactionViewSet, basename='issue-item-inventory-transactions')

# ------Dispense Transaction-------
router.register(r'transaction/dispense/item_info_for_dispense', 
                ItemInformationForDispenseTransactionViewSet,
         basename='item_info_for_dispense-inventory-transactions')
router.register(r'transaction/dispense', DispenseInventoryTransactionViewSet, basename='dispense-inventory-transactions')


# -------Person-----
router.register(r'department', DepartmentViewSet, basename='department')
router.register(r'person_type', PersonTypeViewSet,basename='person-type')
router.register(r'person', PersonViewSet,basename='person')


# --------Prescription---------
router.register(r'prescription', PrescriptionViewSet, basename='prescription')
router.register(r'prescription-with-stock-detail-for-dispense', PrescriptionViewSetForDispense, basename='prescription-with-stock-detail')




router.register(r'setup', SetupView, basename='setup')

# --------Utilities---------
router.register(r'id_manager', IdManagerViewSet)
urlpatterns = [
    # path("admin/", admin.site.urls),
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('api/register/', CreateUserView.as_view(), name='register'),
    # --to get all batches of an item
    # path('item/<int:item_id>/batches', ItemBatchViewSet.as_view({'get': 'item_batches_by_item_id'}), name='item-batches'),
    # # --to get a specific batch of an item
    # re_path(r'^item/(?P<item_id>[0-9a-f-]+)/batches/$', ItemBatchViewSet.as_view({'get': 'item_batches_by_item_id'}), name='item-batches'),
    re_path(r'^item/(?P<item_id>[0-9a-f-]+)/batches/$', ItemBatchViewSet.as_view({'get': 'item_batches_by_item_id', 'post': 'create'}), name='item-batches'),

    path('item/<uuid:item_id>/<str:batch_id>/', ItemBatchViewSet.as_view({'get': 'retrieve_batch'}), name='item-batch-detail'),
    
    path('transaction/<uuid:pk>/', ItemTransactionsView.as_view({'get':'retrieve'}), name='item-transactions-detail'),
    
    re_path(r'^item/(?P<item_id>[0-9a-f-]+)/batches/$', ItemBatchViewSet.as_view({'get': 'item_batches_by_item_id'}), name='item-batches'),
   
  
    path('', include(router.urls)),
]
