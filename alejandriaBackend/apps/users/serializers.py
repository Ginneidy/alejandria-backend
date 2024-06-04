from rest_framework import serializers
from .models import FavoriteList, Cart, Comment
from apps.comon import UserSerializer
from apps.books.serializers import BookSerializer


class FavoriteListSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteList
        fields = "__all__"


class CartReadSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = "__all__"


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
