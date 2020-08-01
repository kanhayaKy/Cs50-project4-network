from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Listing(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE , related_name= "listing")
    title = models.CharField(max_length = 64)
    description = models.CharField(max_length = 256) 
    starting_bid = models.FloatField()
    category = models.CharField(max_length = 64 , default=None , blank = True,null=True)
    image_url = models.URLField(blank=True)
    date = models.DateTimeField(auto_now_add = True)
    bidder_id = models.IntegerField(blank=True,default=None,null=True)
    isactive = models.BooleanField(default=True)
    


    def __str__(self):
        return f"{self.title} by {self.user}"



class Comment(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE , related_name= "comment")
    listing = models.ForeignKey(Listing, on_delete = models.CASCADE , related_name= "comment")
    comment =  models.CharField(max_length = 256) 
    date = models.DateTimeField(auto_now_add = True)

    
    def __str__(self):
        return f"{self.comment} by {self.user} on {self.listing}"

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE , related_name= "bid")
    listing = models.ForeignKey(Listing, on_delete = models.CASCADE , related_name= "bid")
    bid = models.FloatField()
    date = models.DateTimeField(auto_now_add = True)

    
    def __str__(self):
        return f"{self.bid} by {self.user} on {self.listing}"

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE , related_name= "watchlist")
    listing = models.ForeignKey(Listing, on_delete = models.CASCADE , related_name= "watchlist")

    def __str__(self):
        return f"{self.listing} watched by {self.user}"