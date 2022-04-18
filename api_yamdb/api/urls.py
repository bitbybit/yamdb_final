from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import (
    AuthSignUpViewSet,
    AuthTokenViewSet,
    CategoryViewSet,
    CommentViewSet,
    GenreViewSet,
    APIMe,
    ReviewViewSet,
    TitleViewSet,
    UserViewSet,
)

router = SimpleRouter()
router.register("users", UserViewSet)
router.register("titles", TitleViewSet)
router.register("categories", CategoryViewSet)
router.register("genres", GenreViewSet)
router.register(r"titles/(?P<title_id>\d+)/reviews", ReviewViewSet)
router.register(
    r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments",
    CommentViewSet,
)
router.register("auth/signup", AuthSignUpViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("auth/token/", AuthTokenViewSet.as_view()),
    path("users/me", APIMe.as_view()),
]
