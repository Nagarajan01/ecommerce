from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


class Brand(models.Model):
    BRAND_CHOICE = (
        ('Apple', 'Apple'),
        ('Asus', 'Asus'),
        ('Oneplus', 'Oneplus'),
        ('Samsung', 'Samsung')
    )
    brand = models.CharField(choices=BRAND_CHOICE,
                             max_length=100, default='Electronics')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.brand


class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    brand = models.ManyToManyField(Brand, max_length=100)
    image = models.ImageField(upload_to='images')
    in_stock = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=datetime.now)
    product = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    total = models.IntegerField(default=0)
    ordered = models.BooleanField(default=False)

    choices = (
        ('Received', 'Received'),
        ('Scheduled', 'Scheduled'),
        ('Shipped', 'Shipped'),
        ('Failed', 'Failed'),
        ('In Progress', 'In Progress'),
    )

    status = models.CharField(
        max_length=100, choices=choices, default="In Progress")


class Order(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(CartItem)
    start_date = models.DateTimeField(auto_now_add=True)
    total = models.IntegerField(default=0)
    

    def __str__(self):
        return self.user.username


class Wishlist(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    wished_item = models.ForeignKey(Item, on_delete=models.CASCADE)
    slug = models.CharField(max_length=30, null=True, blank=True)
    added_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.wished_item.title
 
class Payment_Detail(models.Model):
    create_time = models.DateField(auto_now=True)
    transaction_id = models.CharField(max_length=30, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment_status = models.CharField(max_length=500, null=True, blank=True)

#  > output be like {'Payment_Status': 'Payment complete.', 'Charge_id': 'ch_3M1vtnSAnvLl9E2S1JH6KXF4'}
