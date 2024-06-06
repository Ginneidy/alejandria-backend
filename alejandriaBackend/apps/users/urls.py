from rest_framework.routers import DefaultRouter
from .views import UserViewSet, RoleViewSet, FavoriteListViewSet, CartViewSet, CommentViewSet


router = DefaultRouter()
router.register(r"users", UserViewSet)
router.register(r"roles", RoleViewSet)
router.register(r"favorites", FavoriteListViewSet)
router.register(r"carts", CartViewSet)
router.register(r"comments", CommentViewSet)

urlpatterns = router.urls