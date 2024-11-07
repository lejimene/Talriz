from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
# Create your models here.

class ItemImage(models.Model):
    item = models.ForeignKey('Item', related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='item_images/')

#Create category for items to be placed in
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
CATEGORY_CHOICES = [
    ('general', "General"),
    # Please add more categories here
]

#Creating items to sell in marketplace
class Item(models.Model):
    STATUS = [ ('active','Active'),('sold','Sold'),('canceled','Canceled'),('ended','Auction_Ended')]
    seller= models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=650)
    #Category allow user to choose three cateogires perhaps? But as admin we can create category
    # categories = models.ManyToManyField(Category, related_name='items', choices=CATEGORY_CHOICES)
    #Price should be filled if the user doesnt want to auction
    price = models.DecimalField(max_digits=12,decimal_places=2,null=True,blank=True)
    #Everything below is auction stuff
    bid_amount =  models.DecimalField(max_digits=12,decimal_places=2,null=True,blank=True)
    buy_out_price =  models.DecimalField(max_digits=12,decimal_places=2,null=True,blank=True)
    auction_end_date = models.DateTimeField(null=True,blank=True)
    auction_end_time = models.TimeField(null=True, blank=True)
    likes = models.ManyToManyField(User, related_name='liked_items',blank=True)
    status = models.CharField(max_length=10, choices=STATUS, default='active')

    def is_auction(self):
        # Tells us if its auction. otherwise assume its not
        return self.bid_amount is not None and self.auction_end_date is not None and self.status == 'active'
    
    def auction_end(self):
        return self.status == 'ended'
    
    def is_sold(self):
        return self.status == 'sold'

    def is_canceled(self):
        return self.status == 'canceled'

    def __str__(self):
        return self.name
    
    def save(self,*args, **kwargs ):
        if not self.price and not self.bid_amount:
            raise ValidationError("You must provide either a price or a bid amount.")
        
        # If auction end date has passed, mark as 'ended' if not sold or canceled
        if self.auction_end_date and self.auction_end_time:
            end_datetime = timezone.datetime.combine(self.auction_end_date, self.auction_end_time)
            if self.status == 'active' and end_datetime <= timezone.now():
                self.status = 'ended'

        
        super().save(*args, **kwargs)
