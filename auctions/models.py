from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    pass

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.CharField(max_length=120)

    def __str__(self):
        return f"{self.category}"

class Listing(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    start_bid = models.PositiveIntegerField(default=0)
    image_url = models.URLField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category_name")

    def __str__(self):
        return f"{self.title} : {self.description} : {self.start_bid} : {self.image_url} : {self.category}"

class Bid(models.Model):
    id = models.AutoField(primary_key=True)
    bid = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.bid}"

class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    comment = models.TextField(blank=True)

    def __str__(self):
        return f"{self.comment}"