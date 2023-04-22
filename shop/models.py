from django.db import models
import datetime
from django.contrib.auth.models import User
import os
# Create your models here.

def getFilename(request,filename):
    now_time = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
    new_filename = "%s%s"%(now_time, filename)
    return os.path.join('upload/', new_filename)

class Catagory(models.Model):
    name = models.CharField(max_length=150,null=False, blank=False)
    image = models.ImageField(upload_to=getFilename,null=True, blank=True)
    discriptions = models.TextField(max_length=500,null=False, blank=False)
    status=models.BooleanField(default=False,help_text="0-show,1-Hidden")
    createdat=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class Product(models.Model):
    catagory = models.ForeignKey(Catagory,on_delete=models.CASCADE,null=False)
    name = models.CharField(max_length=150,null=False, blank=False)
    vendor = models.CharField(max_length=150,null=False, blank=False)
    quantity = models.IntegerField(null=False, blank=False)
    original_price = models.FloatField(null=False, blank=False)
    selling_price = models.FloatField(null=False, blank=False)
    product_image = models.ImageField(upload_to=getFilename,null=True, blank=True)
    discriptions = models.TextField(max_length=500,null=False, blank=False)
    status=models.BooleanField(default=False,help_text="0-show,1-Hidden")
    trending=models.BooleanField(default=False,help_text="0-default,1-Trending")
    createdat=models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=False)
    product = models.ForeignKey(Product,on_delete=models.CASCADE,null=False)
    product_qty = models.IntegerField(null=False, blank=False)
    createdat=models.DateTimeField(auto_now_add=True)
    
    @property
    def total_cost(self):
        return self.product.selling_price * self.product_qty
    
class Favourite(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=False)
    product = models.ForeignKey(Product,on_delete=models.CASCADE,null=False) 
    createdat=models.DateTimeField(auto_now_add=True)
    
    
    
class Order(models.Model):
    email = models.EmailField(max_length=254)
    paid = models.BooleanField(default="False")
    amount = models.IntegerField(default=0)
    description = models.CharField(default=None,max_length=800)
    def __str__(self):
        return self.email