import datetime as dt
from typing import Optional

from django.db.models import Avg
from rest_framework import exceptions, serializers
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import Category, Genre, Title, User

from .validators import validate_username


class UserSerializer(serializers.ModelSerializer):
    def validate_username(self, value):
        return validate_username(value)

    class Meta:
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role",
        )
        read_only_fields = ("role",)
        model = User


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Genre


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Category


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        many=True,
        required=True,
        slug_field="name",
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        required=True,
        slug_field="name",
    )
    rating = serializers.SerializerMethodField()

    @staticmethod
    def get_rating(obj: Title) -> Optional[int]:
        return obj.reviews.aggregate(Avg("score"))["score__avg"]

    @staticmethod
    def process_data(validated_data, instance=None):
        genre = validated_data.pop("genre")

        if instance is None:
            title = Title.objects.create(**validated_data)
        else:
            title = instance

        title.genre.clear()

        for genre_item in genre:
            title.genre.add(genre_item)
            title.save()

        return title

    def create(self, validated_data):
        return self.process_data(validated_data)

    def update(self, instance, validated_data):
        return self.process_data(validated_data, instance)

    def validate_year(self, value):
        if value > dt.datetime.now().year:
            raise serializers.ValidationError(
                "Год выпуска не может быть больше текущего."
            )

        return value

    class Meta:
        fields = (
            "id",
            "name",
            "year",
            "rating",
            "description",
            "genre",
            "category",
        )
        model = Title


class AuthUserSignUpSerializer(serializers.ModelSerializer):
    def validate_username(self, value):
        return validate_username(value)

    class Meta:
        fields = (
            "username",
            "email",
        )
        model = User


class AuthUserTokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True, trim_whitespace=True)
    confirmation_code = serializers.CharField(
        required=True, trim_whitespace=True
    )

    def validate(self, attrs):
        data = attrs

        try:
            user = User.objects.get(
                username=data.get("username"),
                confirmation_code=data.get("confirmation_code"),
            )
        except User.DoesNotExist:
            raise exceptions.NotFound("Пользователь не найден.")

        refresh = RefreshToken.for_user(user)

        return {"token": str(refresh.access_token)}

    class Meta:
        fields = (
            "username",
            "confirmation_code",
        )
        model = User
