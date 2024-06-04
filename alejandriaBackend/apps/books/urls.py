from rest_framework.routers import DefaultRouter
from .views import AuthorViewSet, FormatViewSet, PublisherViewSet, CategoryViewSet, BookViewSet



router = DefaultRouter()
router.register(r"authors", AuthorViewSet)
router.register(r"formats", FormatViewSet)
router.register(r"publishers", PublisherViewSet)
router.register(r"categories", CategoryViewSet)
router.register(r"books", BookViewSet)

urlpatterns = router.urls