from django.contrib.auth.models import AbstractUser
from django.db import models
from djmoney.models.fields import MoneyField
from datetime import datetime,date


class User(AbstractUser):
    pass

    def __str__(self):
        return self.username

class Category(models.Model):
    cat_name = models.CharField(max_length=20, null= True, blank= False)

    def __str__(self):
        return self.cat_name

class Listing(models.Model):
    title = models.CharField(max_length=40, blank=False, null=False)
    text = models.CharField(max_length=200, blank= False, null= True)
    bs_bid = MoneyField(max_digits=19, decimal_places= 4, default_currency= 'BDT')
    img = models.ImageField(null = True, blank = True, upload_to = "listing_img/") 
    owner = models.ForeignKey(User, on_delete= models.CASCADE, null= True, blank=False,related_name='listing_own')
    category = models.ForeignKey(Category, on_delete= models.PROTECT, null=True, blank= False,related_name='category_listing')
    active = models.BooleanField(default=True)
    datefield = models.DateField(auto_now_add=True)
    watchlist = models.ManyToManyField(User, blank=True, related_name='user_watchlist')

    def __str__(self):
        return self.title

class Bid(models.Model):
    listing = models.ForeignKey(Listing,on_delete = models.CASCADE, related_name='listing_bid')
    user = models.ForeignKey(User, on_delete= models.CASCADE, related_name= 'user_bid')
    amount = MoneyField(max_digits=19,decimal_places=2,default_currency= 'BDT')

    def __str__(self):
        return f"{self.listing}--{self.amount}--{self.user}"

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name='user_com')
    listing = models.ForeignKey(Listing, on_delete= models.CASCADE, related_name= 'listing_com')
    text = models.CharField(max_length=100)
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

class Winner(models.Model):
    winner = models.ForeignKey(User, on_delete=models.CASCADE, related_name= 'user_winner')
    hs_bid = models.ForeignKey(Bid, on_delete=models.CASCADE, related_name='winning_bid',null=True)

    def __str__(self):
        return f'{self.winner} - {self.hs_bid}'