from django.contrib.auth.models import AbstractUser
from django.db import models

# Define the category choices
CATEGORIES = [("art", "Art"), ("elec", "Electronics"), ("book_mov_mus", "Books, movies & music"), ("home", "Home & Garden"), ("clothes", "Clothes, shoes & accessoires"), ("sport", "Sporting goods"), ("baby", "Baby essentials"), ("pet", "Pet essentials"), ("other", "Other"), ("cars", "Cars")]



class User(AbstractUser):
    pass

# Auction model
class Listing(models.Model):
    # Fields
    item = models.CharField(max_length=100)
    description = models.TextField()
    starting_bid = models.PositiveIntegerField()
    date = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="my_listings")
    current_price = models.PositiveIntegerField()
    image = models.URLField(blank=True)
    category = models.CharField(max_length=100)
    active = models.BooleanField()
    number_of_bids = models.PositiveIntegerField()
    
    def __str__(self) -> str:
        return f"{self.item}"
    
    def calcMinBid(self) -> int:
        return self.starting_bid +1 if self.starting_bid > self.current_price else self.current_price + 1


class Bid(models.Model):
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="my_bids")
    amount = models.PositiveIntegerField()
    date = models.DateTimeField()


class Category(models.Model):
    category_name = models.CharField(max_length=100, choices=CATEGORIES)
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="list_category_items")


class Comment(models.Model):
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="my_comments")
    comment = models.TextField()
    time = models.DateTimeField()

    def __str__(self) -> str:
        return f"{self.comment}"
    

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="my_watchlist")
    item = models.ForeignKey(Listing, on_delete=models.CASCADE)


class Winners(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="my_wins")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)