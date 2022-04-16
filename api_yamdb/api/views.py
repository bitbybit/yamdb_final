from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from reviews.models import Genre, Review, Title, User
from .filtersets import TitleFilter
from .permissions import IsAdminOrReadOnly
from .serializers import (
    GenreSerializer,
    ReviewSerializer,
    TitleSerializer,
    UserSerializer,
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
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        reviews = title.reviews.all()
        return reviews

    def perform_create(self, serializer):
        author = self.request.user
        title_id = self.kwargs.get("title_id")
        review_exists = Review.objects.filter(author=author, title_id=title_id)
        if not review_exists:
            serializer.save(author=author, title_id=title_id)
        else:
            raise PermissionDenied
