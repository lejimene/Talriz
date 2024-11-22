from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

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
    likes = models.ManyToManyField(User, related_name='liked_items',blank=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
            # Normalize empty strings to None
            self.price = self.price if self.price else None
            self.bid_amount = self.bid_amount if self.bid_amount else None
            self.buy_out_price = self.buy_out_price if self.buy_out_price else None
            
            # Validation: Ensure at least one value is provided
            if not self.bid_amount and not self.price:
                raise ValidationError("You must provide a price or bid amount. Both cannot be left blank.")
            
            super().save(*args, **kwargs)