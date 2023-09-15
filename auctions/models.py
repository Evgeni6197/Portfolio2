from django.contrib.auth.models import AbstractUser
from django.db import models

from .forms import category_choices


class User(AbstractUser):
    pass


class Listing(models.Model):
    title = models.CharField(max_length=64)

    # user, who created  the  listing
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # absolute url path of descriptive image if exists
    image_url = models.URLField(max_length=200, blank=True)

    # filename of descriptive image if exists
    filename = models.CharField(max_length=100, unique=True)
    starting_bid = models.IntegerField()
    category = models.CharField(
        max_length=12, choices=category_choices, default="Others"
    )
    description = models.TextField(blank=True)
    status = models.CharField(
        max_length=1, choices=[("a", "active"), ("n", "non-active")], default="a"
    )
    current_price = models.IntegerField(default=0)

    # name of the user, who made the last bid
    current_bidder = models.CharField(max_length=64, blank=True)

    datetime = models.DateTimeField(null=True)


class Bid(models.Model):
    # listing for that the bid is specified
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")

    # user that made this bid
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # numerical bid value
    amount = models.IntegerField(default=0)

    # auto filling on instantiation
    datetime = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):

    # fields' meaning similar to Bid class

    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    datetime = models.DateTimeField(auto_now_add=True)


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
