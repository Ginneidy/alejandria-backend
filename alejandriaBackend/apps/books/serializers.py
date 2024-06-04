from rest_framework import serializers
from .models import Author, Format, Publisher, Category, Book
from apps.comon import UserSerializer


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"


class FormatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Format
        fields = "__all__"


class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

class BookWriteSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only = True)
    publisher = PublisherSerializer(read_only = True)
    class Meta:
        model = Book
        fields = "__all__"
        
        
class BookSerializer(serializers.ModelSerializer):
    format = serializers.CharField(source="format.description")
    author = serializers.CharField(source="author.name", allow_null=True)
    publisher = serializers.CharField(source="publisher.name_publisher", allow_null=True)
    seller = UserSerializer()
    categories = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = "__all__"
