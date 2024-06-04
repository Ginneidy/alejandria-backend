from rest_framework.routers import DefaultRouter
from .views import SaleViewSet, PurchaseViewSet


router = DefaultRouter()
router.register(r"sales", SaleViewSet)
router.register(r"purchases", PurchaseViewSet)

urlpatterns = router.urls