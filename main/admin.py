from django.contrib import admin
from .models import *


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['email', 'username', 'num_ads']


admin.site.register(CustomUser, CustomUserAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'category', 'price', 'retailer', 'date_added']

class CloudinaryURLAdmin(admin.ModelAdmin):
    list_display = ['productt', 'link']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_code', 'buyer', 'timestamp', 'total_price']


class MessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receipent', 'content']


admin.site.register(Product, ProductAdmin)
admin.site.register(Review)
admin.site.register(Reply)
admin.site.register(CartItem)
admin.site.register(Order, OrderAdmin)
admin.site.register(CloudinaryURLs, CloudinaryURLAdmin)
admin.site.register(Message, MessageAdmin)
