from rest_framework.routers import SimpleRouter

from shop.views import ProductViewSet, CategoryViewSet, OrderViewSet, UserViewSet

router = SimpleRouter()
router.register("products", ProductViewSet, basename="Product")
router.register("categories", CategoryViewSet, basename="Category")
router.register("orders", OrderViewSet, basename="Order")
router.register("users", UserViewSet, basename="User")

urls = router.urls
