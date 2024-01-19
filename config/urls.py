from django.urls import include, path
from rest_framework.routers import DefaultRouter

from features.item.unit_of_measurement.views import UnitOfMeasurementViewSet
from features.item.item_category.views import ItemCategoryViewSet
from features.item.item_type.views import ItemTypeViewSet


from rest_framework_swagger.views import get_swagger_view

router = DefaultRouter()
router.register(r'item/units-of-measurement', UnitOfMeasurementViewSet)
router.register(r'item/item_category', ItemCategoryViewSet)
router.register(r'item/item_type', ItemTypeViewSet)


schema_view = get_swagger_view(title='API Docs')

urlpatterns = [
    path('', include(router.urls)),
    path('docs/', schema_view),
]