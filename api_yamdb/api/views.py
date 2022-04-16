from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from reviews.models import Title, User, Genre

from .filtersets import TitleFilter
from .serializers import (
    TitleSerializer,
    UserSerializer,
    GenreSerializer,
)

"""
TODO: после реализации аутентификации протестировать работу эндпоинта users/me,
поле role должно быть доступно только при GET запросе, юзер не может менять
роль. можно для PATCH запроса использовать отдельный сериализатор, в котором
поле role будет отсутствовать.
"""


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ("username",)
    lookup_field = "username"

    @action(detail=True, methods=["get", "patch"])
    def me(self, request):
        user = self.request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = TitleFilter


class GenreViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter, )
    search_fields = ("name",)
