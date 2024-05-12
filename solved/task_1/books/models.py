from django.db import models


class Book(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    genre = models.CharField(max_length=100)
    price = models.IntegerField()

    def __str__(self):
        return self.name
