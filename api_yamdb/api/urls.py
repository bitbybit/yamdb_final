from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import TitleViewSet, UserViewSet

router = SimpleRouter()
router.register("users", UserViewSet)
router.register("titles", TitleViewSet)

urlpatterns = [path("", include(router.urls))]
