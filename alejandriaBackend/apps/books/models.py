from django.db import models
from apps.baseModel import BaseModel

class Author(BaseModel):
    name = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = "author"


class Format(BaseModel):
    description = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'format'


class Publisher(BaseModel):
    name_publisher = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'publisher'


class Category(BaseModel):
    description = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'category'
        

class Book(BaseModel):
    title = models.CharField(max_length=40)
    price = models.IntegerField()
    description = models.TextField()
    pub_year = models.CharField(max_length=5, blank=True, null=True)
    pages = models.IntegerField()
    front_page = models.CharField(blank=True, null=True)
    format = models.ForeignKey(Format, models.DO_NOTHING)
    author = models.ForeignKey(Author, models.DO_NOTHING, blank=True, null=True)
    publisher = models.ForeignKey(Publisher, models.DO_NOTHING, blank=True, null=True)
    seller = models.ForeignKey("users.User", models.DO_NOTHING)
    categories = models.ManyToManyField(Category, db_table="book_category")
    status = models.CharField()

    class Meta:
        managed = False
        db_table = 'book'
    
        
