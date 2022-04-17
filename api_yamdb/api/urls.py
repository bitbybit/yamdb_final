from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import (
    AuthSignUpViewSet,
    AuthTokenViewSet,
    CategoryViewSet,
    GenreViewSet,
    ReviewViewSet,
    TitleViewSet,
    UserViewSet,
)

router = SimpleRouter()
router.register("users", UserViewSet)
router.register("titles", TitleViewSet)
router.register("categories", CategoryViewSet)
router.register("genres", GenreViewSet)
router.register(
    r"titles/(?P<title_id>\d+)/reviews", ReviewViewSet, basename="review"
)
router.register("auth/signup", AuthSignUpViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("auth/token/", AuthTokenViewSet.as_view()),
]
