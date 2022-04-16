from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import CategoryViewSet, TitleViewSet, UserViewSet

router = SimpleRouter()
router.register("users", UserViewSet)
router.register("titles", TitleViewSet)
router.register("categories", CategoryViewSet)

urlpatterns = [path("", include(router.urls))]
