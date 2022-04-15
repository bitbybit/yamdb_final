from rest_framework import serializers
from reviews.models import User, Genre, Title, Category, Review


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = '__all__'
