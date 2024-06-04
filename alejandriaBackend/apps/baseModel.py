from django.db import models


class BaseModel(models.Model):
    id = models.AutoField(primary_key=True)
    created_date = models.DateTimeField(auto_now_add=True)
    deleted_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        abstract = True
