import datetime as dt
from typing import Optional

from django.db.models import Avg
from rest_framework import serializers
from reviews.models import Category, Genre, Title, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role",
        )
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

    def validate(self, attrs):
        if attrs["year"] > dt.datetime.now().year:
            raise serializers.ValidationError(
                "Год выпуска не может быть больше текущего."
            )

        return attrs

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
