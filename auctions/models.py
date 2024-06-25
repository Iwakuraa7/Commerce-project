from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    watchlist = models.ManyToManyField('Listing', blank=True, related_name="watchlisted_by")

    def __str__(self):
        return f"{self.id} : {self.username} : {self.password} : {self.watchlist}"

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.CharField(max_length=120)

    def __str__(self):
        return f"{self.category}"

class Listing(models.Model):
    id = models.AutoField(primary_key=True)
    # to know the creator of the listing => no bidding, (+) closing the listing
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings", default=2)
    # to know the winner of the listing
    highest_bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="winners", default=1)
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    start_bid = models.PositiveIntegerField(default=0)
    image_url = models.URLField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category_name")
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} : {self.description} : {self.start_bid} : {self.image_url} : {self.category}"

class Bid(models.Model):
    id = models.AutoField(primary_key=True)
    # to know to which listing bids belong to
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids", default=1)
    bid = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.bid}"

class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    # to know to which listing comments belong to
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments", default=1)
    comment = models.TextField(blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="users_comments", default=1)

    def __str__(self):
        return f"{self.comment}"