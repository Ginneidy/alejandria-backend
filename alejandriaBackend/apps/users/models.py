from django.db import models
from apps.books.models import Book
from apps.baseModel import BaseModel


class Role(BaseModel):
    description = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = "role"
        
        
class User(BaseModel):
    user_name = models.CharField(max_length=50)
    email_address = models.CharField(unique=True, max_length=40)
    user_password = models.CharField()
    street_address = models.CharField(blank=True, null=True)
    score = models.IntegerField(blank=True, null=True)
    roles = models.ManyToManyField(Role, db_table="user_role")

    class Meta:
        managed = False
        db_table = "user"




class FavoriteList(BaseModel):
    user = models.ForeignKey(User, models.DO_NOTHING)
    books = models.ManyToManyField(Book, db_table="favorite_books")

    class Meta:
        managed = False
        db_table = "favorite_list"


class Cart(BaseModel):
    total_amount = models.IntegerField()
    user = models.ForeignKey(User, models.DO_NOTHING)
    books = models.ManyToManyField(Book, db_table="cart_book")

    class Meta:
        managed = False
        db_table = "cart"


class Comment(BaseModel):
    user = models.ForeignKey(
        User,
        models.DO_NOTHING,
        db_comment="El usuario al que le hicieron el comentario",
    )
    observation = models.TextField()

    class Meta:
        managed = False
        db_table = "comment"
