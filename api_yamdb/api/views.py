from rest_framework import viewsets, filters
from reviews.models import User, Genre, Title, Category, Review
from .serializers import (
    GenreSerializer
)


class GenreViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter, )
    search_fields = ("name",)
