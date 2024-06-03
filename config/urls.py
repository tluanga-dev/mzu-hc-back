from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from features.id_manager.views import IdManagerViewSet
from features.inventory_transaction.dispense_transaction.views import DispenseInventoryTransactionViewSet
from features.inventory_transaction.indent_transaction.views import IndentInventoryTransactionViewSet
from features.inventory_transaction.inventory_transaction.views import ItemTransactionsView
from features.inventory_transaction.issue_transaction.views import IssueItemInventoryTransactionViewSet
from features.item.views import (
    ItemBatchViewSet, ItemCategoryViewSet, ItemDetailForReportViewSet, ItemTypeViewSet, 
    ItemViewSet, ItemWithStockInfoViewSet, UnitOfMeasurementViewSet
)
from features.medicine.views import MedicineDosageViewSet
from features.patient.views import PatientViewSet
from features.person.views import EmployeeDependentViewSet, EmployeeViewSet, MZUOutsiderViewSet, StudentViewSet
from features.prescription.views import PrescriptionViewSet
from features.setup.views import SetupView
from features.supplier.views import SupplierViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

router = DefaultRouter()

# Registering all viewsets with the router
router.register(r'item/item_with_stock_info', ItemWithStockInfoViewSet, basename='item-with-stock-info')
router.register(r'item/units-of-measurement', UnitOfMeasurementViewSet, basename='unit-of-measurement')
router.register(r'item/item_category', ItemCategoryViewSet)
router.register(r'item/item_type', ItemTypeViewSet)
router.register(r'item', ItemViewSet, basename='item')
router.register(r'item_detail_for_report', ItemDetailForReportViewSet, basename='item-detail-for-report')
router.register(r'medicine/medicine_dosage', MedicineDosageViewSet)
router.register(r'supplier', SupplierViewSet)
router.register(r'transaction/indent', IndentInventoryTransactionViewSet, basename='indent-inventory-transactions')
router.register(r'transaction/issue_item', IssueItemInventoryTransactionViewSet, basename='issue-item-inventory-transactions')
router.register(r'transaction/dispense', DispenseInventoryTransactionViewSet, basename='dispense-inventory-transactions')
router.register(r'employee', EmployeeViewSet, basename='employee')
router.register(r'employee_dependent', EmployeeDependentViewSet, basename='employee-dependent')
router.register(r'student', StudentViewSet, basename='student')
router.register(r'mzu_outsider', MZUOutsiderViewSet, basename='mzu-outsider')
router.register(r'patient', PatientViewSet, basename='patient')
router.register(r'prescription', PrescriptionViewSet, basename='prescription')
router.register(r'setup', SetupView, basename='setup')
router.register(r'id_manager', IdManagerViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),

    # JWT Authentication URLs
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # Item Batch Related URLs
    re_path(r'^item/(?P<item_id>[0-9a-f-]+)/batches/$', ItemBatchViewSet.as_view({'get': 'item_batches_by_item_id', 'post': 'create'}), name='item-batches'),
    # Changed to UUID pattern for item_id and string pattern for batch_id
    path('item/<uuid:item_id>/<str:batch_id>/', ItemBatchViewSet.as_view({'get': 'retrieve_batch'}), name='item-batch-detail'),

    # Item Detail for Report URL
    path('item_detail_for_report/<int:pk>/', ItemDetailForReportViewSet.as_view({'get': 'revieve_item_detail_by_batch_id'}), name='item_detail_for_report_api'),

    # Transaction Detail URL with UUID pattern
    path('transaction/<uuid:pk>/', ItemTransactionsView.as_view({'get':'retrieve'}), name='item-transactions-detail'),

    # Removed redundant pattern
    # re_path(r'^item/(?P<item_id>[0-9a-f-]+)/batches/$', ItemBatchViewSet.as_view({'get': 'item_batches_by_item_id'}), name='item-batches'),

    # Include all routes defined in the router
    path('', include(router.urls)),
]
