from django.urls import include, path
from rest_framework.routers import DefaultRouter
from features.item.item.views import ItemViewSet
from features.item.medicine_dosage_duration.views import MedicineDosageDurationViewSet

from features.item.unit_of_measurement.views import UnitOfMeasurementViewSet
from features.item.item_category.views import ItemCategoryViewSet
from features.item.item_type.views import ItemTypeViewSet

# --------Transactions---------
from features.transaction.item_stock_info.views import ItemStockInfoViewSet


from rest_framework_swagger.views import get_swagger_view

router = DefaultRouter()
router.register(r'item/units-of-measurement', UnitOfMeasurementViewSet)
router.register(r'item/item_category', ItemCategoryViewSet)
router.register(r'item/item_type', ItemTypeViewSet)
router.register(r'transaction/item_stock_info', ItemStockInfoViewSet)
router.register(r'item', ItemViewSet)
router.register(r'item/medicine_dosage_duration', MedicineDosageDurationViewSet)


schema_view = get_swagger_view(title='API Docs')

urlpatterns = [
    path('', include(router.urls)),
    path('docs/', schema_view),
]