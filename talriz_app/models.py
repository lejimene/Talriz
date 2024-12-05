from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
# Create your models here.

class ItemImage(models.Model):
    item = models.ForeignKey('Item', related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='item_images/')

class Bidder(models.Model):
    item = models.ForeignKey('Item', related_name='bidders', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bid_amount = models.DecimalField(max_digits=12, decimal_places=2)
    bid_time = models.DateTimeField(auto_now_add=True)  # set time immedtaily

    def __str__(self):
        return f"{self.user.username} bid {self.bid_amount} on {self.item.name} at {self.bid_time}"


#Creating items to sell in marketplace
class Item(models.Model):
    STATUS = [
        ('active', 'Active'),
        ('sold', 'Sold'),
        ('canceled', 'Canceled'),
        ('ended', 'Auction_Ended')
    ]
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=650)
    price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    
    # Auction fields
    is_auction = models.BooleanField(default=False)
    bid_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    buy_out_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    auction_end_datetime = models.DateTimeField(null=True, blank=True)
    likes = models.ManyToManyField(User, related_name='liked_items', blank=True)
    status = models.CharField(max_length=10, choices=STATUS, default='active')
    #winner = models.ForeignKey(User,related_name="items_won", null=True, blank=True, on_delete=models.SET_NULL)


    def auction_end(self):
        return self.status == 'ended'

    def is_sold(self):
        return self.status == 'sold'

    def is_canceled(self):
        return self.status == 'canceled'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Price and bid checks
        self.price = self.price if self.price else None
        self.bid_amount = self.bid_amount if self.bid_amount else None
        self.buy_out_price = self.buy_out_price if self.buy_out_price else None

        # Validation for auction items if true check for all fields to be something
        if self.is_auction:
            if not self.auction_end_datetime:
                raise ValidationError("Auction items must have an end date and time.")
            if not self.bid_amount:
                raise ValidationError("Auction items must have a starting bid.")
        elif not self.price:
            raise ValidationError("Non-auction items must have a price.")

        super().save(*args, **kwargs)

class Message(models.Model):
    buyer = models.TextField()
    seller = models.TextField()
    data = models.TextField()
    id = models.TextField(primary_key=True)

    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.buyer}: {self.data}"
    