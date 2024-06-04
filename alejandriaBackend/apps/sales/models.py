from django.db import models
from apps.baseModel import BaseModel
from apps.books.models import Book
from apps.users.models import User


class Sale(BaseModel):
    total_amount = models.IntegerField()
    date_sale = models.DateTimeField()
    seller = models.ForeignKey(User, models.DO_NOTHING)
    book = models.ForeignKey(Book, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "sale"


class Purchase(BaseModel):
    total_amount = models.IntegerField()
    date_purchase = models.DateTimeField()
    user = models.ForeignKey(User, models.DO_NOTHING)
    books = models.ManyToManyField(Book, db_table="book_purchase")
    

    class Meta:
        managed = False
        db_table = "purchase"
