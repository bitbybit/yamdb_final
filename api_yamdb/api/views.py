from uuid import uuid4

from django.core.mail import send_mail
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from reviews.models import Genre, Title, User

from .filtersets import TitleFilter
from .permissions import IsAdminOrReadOnly
from .serializers import (
    AuthUserSignUpSerializer,
    AuthUserTokenSerializer,
    GenreSerializer,
    TitleSerializer,
    UserSerializer,
)
from .viewsets import CreateModelViewSet

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
    permission_classes = (IsAdminOrReadOnly,)
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)


class AuthSignUpViewSet(CreateModelViewSet):
    permission_classes = (permissions.AllowAny,)
    queryset = User.objects.all()
    serializer_class = AuthUserSignUpSerializer

    @staticmethod
    def generate_confirmation_code() -> str:
        return uuid4().hex

    @staticmethod
    def send_confirmation_code(email_to: str, confirmation_code: str):
        email_from = "api@yamdb.yamdb"
        subject = "Код подтверждения"

        send_mail(
            subject,
            confirmation_code,
            email_from,
            [email_to],
            fail_silently=False,
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        confirmation_code = self.generate_confirmation_code()

        try:
            user = User.objects.get(
                username=serializer.initial_data.get("username"),
                email=serializer.initial_data.get("email"),
            )
            user.confirmation_code = confirmation_code
            user.save()
        except User.DoesNotExist:
            serializer.is_valid(raise_exception=True)
            serializer.save(confirmation_code=confirmation_code)

        self.send_confirmation_code(
            serializer.initial_data["email"], confirmation_code
        )

        headers = self.get_success_headers(serializer.initial_data)

        return Response(
            serializer.initial_data, status=status.HTTP_200_OK, headers=headers
        )


class AuthTokenViewSet(TokenObtainPairView):
    serializer_class = AuthUserTokenSerializer
