from rest_framework import serializers
from .models import Sale, Purchase
from apps.comon import UserSerializer
from apps.books.serializers import BookSerializer


class SaleSerializer(serializers.ModelSerializer):
    seller = UserSerializer()
    book = serializers.CharField(source="book.title")
    class Meta:
        model = Sale
        fields = "__all__"


class PurchaseSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Purchase
        fields = "__all__"
