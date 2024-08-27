from itertools import product
from django.db import models

from core.models import User
from shop.models import Product
import uuid
# Create your models here.


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    products = models.ManyToManyField(Product, through='CartItems', related_name="cartItems")
    
    def __str__(self):
        return f"Cart of {self.user.email}"
    
# class CartItem(models.Model):
#     cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
#     products = models.ManyToManyField(Product)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     quantity = models.PositiveIntegerField(default=1)
    
#     def __str__(self):
#         return f"Items of {self.cart} - Products: {self.products.all()}"
    
    
class CartItems(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    products = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cart_id = models.ForeignKey(Cart, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='OrderItems', related_name="orderItems")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    total = models.DecimalField(max_digits=10, decimal_places=0)
    paid = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Order: {self.id} - Cart: {self.cart_id}"
    
class OrderItems(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    products = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
class History(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"History of {self.user} for order {self.order.id}"