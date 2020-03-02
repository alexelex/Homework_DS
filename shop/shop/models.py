from django.conf import settings
from django.db import models

class Products(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=200)
    category = models.CharField(max_length=200)
    time_create = models.DateTimeField(auto_now_add=True)
    time_modified = models.DateTimeField(auto_now=True)
