import re
import hashlib

from datetime import datetime
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from django.db import transaction

from .models import User, Role, FavoriteList, Cart, Comment
from .serializers import (
    FavoriteListSerializer,
    CartSerializer,
    CartReadSerializer,
    CommentSerializer,
)
from apps.comon import UserSerializer, RoleSerializer


# Function for validating email
def is_valid_email(email):
    return re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email)


# Function for user password hashing
def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # Action to handle user login
    # /api/auth/users/login/
    @action(detail=False, methods=["POST"])
    def login(self, request, *args, **kwargs):
        print(f"data: {request.data}")
        email_address = request.data.get("email_address")
        user_password = request.data.get("user_password")

        # Encrypt the user-provided password with MD5
        user_password_md5 = hash_password(user_password)

        user = User.objects.filter(email_address=email_address)

        if user.exists():
            # Check if the provided password matches the one stored in the database
            if user_password_md5 == user.first().user_password:
                userData = UserSerializer(user.first()).data
                # Generate token
                refresh = RefreshToken.for_user(user.first())
                token = {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                }

                response_data = {"token": token, "user": userData}
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"error": "Contraseña incorrecta"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(
                {
                    "error": "No existe ningún usuario con esa dirección de correo electrónico"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

    # Action to handle user registration
    # /api/users/register/
    @action(detail=False, methods=["POST"])
    def register(self, request):
        data = request.data

        # Validation of required fields
        required_fields = [
            "user_name",
            "email_address",
            "user_password",
        ]

        for field in required_fields:
            if not data.get(field):
                return Response(
                    {"error": f"{field.replace('_', ' ').capitalize()} is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        # Validation of name and last name
        name_regex = r"^[A-Za-zÀ-ÖØ-öø-ÿ]+(?:\s+[A-Za-zÀ-ÖØ-öø-ÿ]+)*$"
        if not re.match(name_regex, data.get("user_name")):
            return Response(
                {"error": "Nombre de usuario no válido"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Validation of email
        email = data.get("email_address")
        if not is_valid_email(email):
            return Response(
                {"error": "Dirección de correo electrónico no válida"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Validation of password
        password = data.get("user_password")

        if not password:
            return Response(
                {"error": "Se requiere contraseña"}, status=status.HTTP_400_BAD_REQUEST
            )
        if not (
            any(char.isdigit() for char in password)
            and any(char.islower() for char in password)
            and any(char.isupper() for char in password)
        ):
            return Response(
                {
                    "error": "La contraseña debe contener al menos un número, una letra mayúscula y una letra minúscula."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Encrypting the password
        hashed_password = hash_password(password)

        # TODO: Implementar el correo de activación
        """ # Activation code generation
        activation_code = "".join(
            random.choices(string.ascii_letters + string.digits, k=5)
        ) """

        # User creation
        created_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S %z")

        with transaction.atomic():
            serializer = UserSerializer(
                data={
                    "user_name": data.get("user_name"),
                    "email_address": data.get("email_address"),
                    "user_password": hashed_password,
                    "created_date": created_date,
                }
            )

            if serializer.is_valid():
                user = serializer.save()

                # Assigning the role
                role_id = int(
                    data.get("role", 1)
                )  # If the value is not present, 1 is assigned as the default value
                role = Role.objects.get(pk=role_id)
                user.roles.add(role)

                # TODO: Implementar esto
                """ 
                # Sending activation email
                send_activation_mail(user.email_address, activation_code) """
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer


class FavoriteListViewSet(viewsets.ModelViewSet):
    queryset = FavoriteList.objects.all()
    serializer_class = FavoriteListSerializer

    # Action to get favorite lists by user ID
    # /api/favorites/get_favorite_lists/
    # /api/favorites/get_favorite_lists/<user_id>/
    @action(detail=True, methods=["GET"])
    def get_favorite_lists(self, request, pk=None):
        print(f"pk: {pk}")
        user = self.get_object()
        favorite_lists = FavoriteList.objects.filter(user=user)
        serializer = FavoriteListSerializer(favorite_lists, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def get_serializer_class(self):
        if self.action == "create":
            return CartSerializer
        return CartReadSerializer

    # Action to add a book to the cart
    # /api/carts/add_to_cart/
    @action(detail=False, methods=["POST"])
    def add_to_cart(self, request):
        data = request.data
        print(f"data: {data}")
        user_id = data.get("user")
        book_id = data.get("books")[0]

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {"error": "Usuario no encontrado"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Check if the user already has a cart
        cart = Cart.objects.filter(user=user).first()

        if not cart:
            # Create a new cart for the user
            cart = Cart.objects.create(user=user, total_amount=0)

        # Check if the book is already in the cart
        if cart.books.filter(id=book_id).exists():
            return Response(
                {"error": "El libro ya está en el carrito"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Add the book to the cart
        cart.books.add(book_id)

        return Response(
            {"message": "Libro agregado al carrito exitosamente"},
            status=status.HTTP_200_OK,
        )

    # Action to get cart by user ID
    # /api/carts/get_cart_by_user/
    @action(detail=False, methods=["GET"])
    def get_cart_by_user(self, request):
        user_id = request.query_params.get("user_id")

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {"error": "Usuario no encontrado"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        cart = Cart.objects.filter(user=user).first()

        if not cart:
            return Response(
                {"message": "El usuario no tiene un carrito"},
                status=status.HTTP_200_OK,
            )

        serializer = CartReadSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
