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

    def create(self, request, *args, **kwargs):
        print(f"request.data: {request.data}")
        author_data = request.data.get("author")
        publisher_data = request.data.get("publisher")
        print(f"author_data: {author_data}")

        author_serializer = AuthorSerializer(data=author_data)
        publisher_serializer = PublisherSerializer(data=publisher_data)

        if author_serializer.is_valid() and publisher_serializer.is_valid():
            author = author_serializer.save()
            publisher = publisher_serializer.save()

            book_data = {
                "format": request.data.get("format"),
                "author": author.id,
                "publisher": publisher.id,
                "seller": int(request.data.get("seller")),
                "categories": request.data.get("categories"),
                "title": request.data.get("title"),
                "price": int(request.data.get("price")),
                "description": request.data.get("description"),
                "pub_year": int(request.data.get("pub_year")),
                "pages": int(request.data.get("pages")),
                "status": "inactive",
            }

            book_serializer = BookWriteSerializer(data=book_data)

            if book_serializer.is_valid():
                book = book_serializer.save()
                # Usar BookSerializer para la respuesta
                response_serializer = BookSerializer(book)
                return Response(
                    response_serializer.data, status=status.HTTP_201_CREATED
                )
            else:
                return Response(
                    book_serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )
        else:
            errors = {}
            if not author_serializer.is_valid():
                errors["author"] = author_serializer.errors
            if not publisher_serializer.is_valid():
                errors["publisher"] = publisher_serializer.errors
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

    # Custom action
    # PUT /books/{pk}/change_status/
    # Custom action
    # PUT /books/{pk}/change_status/
    @action(detail=True, methods=["put"])
    def change_status(self, request, pk=None):
        try:
            print(f"request.data: {request.data}")
            print("PK = ", pk)
            book = self.get_object()
            book.status = "active"
            book.save()
            return Response({"status": "active"}, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"Error: {str(e)}")
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # Custom action

    # DELETE /books/{pk}/delete_if_not_test/
    @action(detail=True, methods=["DELETE"])
    def delete_if_not_test(self, request, pk=None):
        book = self.get_object()
        if book.title != "test":
            book.delete()
            return Response(
                {"message": "Book deleted"}, status=status.HTTP_204_NO_CONTENT
            )
        else:
            return Response(
                {"message": "Cannot delete test book"},
                status=status.HTTP_400_BAD_REQUEST,
            )
