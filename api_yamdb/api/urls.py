from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import (
    AuthSignUpViewSet,
    AuthTokenViewSet,
    GenreViewSet,
    TitleViewSet,
    UserViewSet,
)

router = SimpleRouter()
router.register("users", UserViewSet)
router.register("titles", TitleViewSet)
router.register("genres", GenreViewSet)
router.register("auth/signup", AuthSignUpViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("auth/token/", AuthTokenViewSet.as_view()),
]
