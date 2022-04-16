from django.urls import include, path
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import TitleViewSet, UserViewSet

router = SimpleRouter()
router.register("users", UserViewSet)
router.register("titles", TitleViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path(
        "auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"
    ),
]
