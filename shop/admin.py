from django.contrib import admin
from shop.models import Category, Product, Order, OrderItem

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
