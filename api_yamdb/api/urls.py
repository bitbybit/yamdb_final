from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import GenreViewSet, ReviewViewSet, TitleViewSet, UserViewSet

router = SimpleRouter()
router.register("users", UserViewSet)
router.register("titles", TitleViewSet)
router.register("genres", GenreViewSet)
router.register(
    r"titles/(?P<title_id>\d+)/reviews", ReviewViewSet, basename="review"
)
urlpatterns = [path("", include(router.urls))]
