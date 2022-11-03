from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Brand)


class item(admin.ModelAdmin):
    list_display = ('id', 'title', 'price',
                    'discount_price', 'image', 'in_stock')


admin.site.register(Item, item)


class My_cart(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at',
                    'product', 'quantity', 'ordered', 'total')


admin.site.register(CartItem, My_cart)


class Myorder(admin.ModelAdmin):
    list_display = (
        'user', 'start_date', 'total')


admin.site.register(Order, Myorder)


class MyWishlist(admin.ModelAdmin):
    list_display = (
        'user', 'wished_item', 'slug', 'added_date')


admin.site.register(Wishlist, MyWishlist)
