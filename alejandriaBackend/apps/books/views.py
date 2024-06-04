from rest_framework import viewsets
from .models import Author, Format, Publisher, Category, Book
from .serializers import (
    AuthorSerializer,
    FormatSerializer,
    PublisherSerializer,
    CategorySerializer,
    BookSerializer,
    BookWriteSerializer,
)
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class FormatViewSet(viewsets.ModelViewSet):
    queryset = Format.objects.all()
    serializer_class = FormatSerializer


class PublisherViewSet(viewsets.ModelViewSet):
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_serializer_class(self):
        if self.action == "create":
            return BookWriteSerializer
        return BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_serializer_class(self):
        if self.action == "create":
            return BookWriteSerializer
        return BookSerializer

    # Custom action
    # PUT /books/{pk}/change_status/
    @action(detail=True, methods=["PUT"])
    def change_status(self, request, pk=None):
        book = self.get_object()
        book.status = "active"
        book.save()
        return Response({"status": "active"}, status=status.HTTP_200_OK)
