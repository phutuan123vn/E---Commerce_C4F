from django.contrib import admin
from .models import Cart, CartItems, Order, OrderItems
# Register your models here.


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    pass


@admin.register(CartItems)
class CartItemsAdmin(admin.ModelAdmin):
    pass


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass

@admin.register(OrderItems)
class OrderItemsAdmin(admin.ModelAdmin):
    pass