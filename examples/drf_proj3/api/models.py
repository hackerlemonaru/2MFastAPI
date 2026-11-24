from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=40)
    pages = models.IntegerField(default=100)
    price = models.FloatField(null=True, blank=True)
    in_stock = models.BooleanField(default=True)
    note = models.TextField(blank=True)
