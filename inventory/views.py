from pprint import pprint
from uu import Error

from django.db import transaction
from django.db.models import (Case, F, IntegerField, OuterRef, Prefetch,
                              Subquery, Sum, Value, When)
from django.shortcuts import redirect, render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import User
from inventory.serializers import CartSerializer, OrderItemsSerializer
from shop.models import Product

from .models import Cart, CartItems, Order, OrderItems


# Create your views here.
class CartItemView(APIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = CartSerializer
    
    # @permission_classes([IsAuthenticated])
    def get(self, request: Request):
        if request.user.is_anonymous:
            return Response({"cardItems": []})
        existed = Cart.objects.filter(user=request.user).exists()
        if not existed:
            cart = Cart.objects.create(user=request.user)
            serializer = CartSerializer(cart) 
            return Response({"cartItems": serializer.data})
        cartItems = CartItems.objects.filter(products=OuterRef('pk')).values('quantity')
        products_qs = Product.objects.order_by('id').annotate(quantities=Subquery(cartItems))
        products_prefetch = Prefetch('products', queryset=products_qs.only('id', 'name', 'price'))
        cart = Cart.objects.filter(user=request.user).prefetch_related(products_prefetch).only('id', 'user', 'products')
        # products_prefetch = Prefetch('products', queryset=Product.objects.order_by('id').only('id', 'name', 'price'))
        # cart = Cart.objects.filter(user=request.user).prefetch_related(products_prefetch).only('id', 'user', 'products').annotate(total=Sum(F('products__price') * F('cartitems__quantity'), output_field=IntegerField()))
        serializer = CartSerializer(cart,many=True) 
        return Response({"cartItems": serializer.data})
    
    @permission_classes([IsAuthenticated])
    def post(self, request: Request):
        cart = Cart.objects.get(user=request.user)
        product_id = request.data.get('product_id', None)
        if not product_id: raise ValueError("Product ID is required")
        quantity = request.data.get('quantity', 1)
        if CartItems.objects.filter(cart=cart, products=product_id).exists():
            cart_item = CartItems.objects.get(cart=cart, products=product_id)
            cart_item.quantity = F('quantity') * 0 + quantity
            cart_item.save()
        else:
            product = Product.objects.filter(id=product_id).get()
            cart.products.add(product, through_defaults={'quantity': quantity})
        response = self.get(request)
        response.status_code = status.HTTP_201_CREATED
        return response

    
    
    @permission_classes([IsAuthenticated])
    def delete(self, request: Request):
        cartItems = CartItems.objects.filter(cart__user=request.user)
        cartItems.delete()
        return redirect('cart')
    
    
    @permission_classes([IsAuthenticated])
    def put(self, request: Request, pk):
        # cart_item = CartItem.objects.get(id=pk)
        # cart_item.quantity = request.data.get('quantity')
        # cart_item.save()
        # serializer = CartItemSerializer(cart_item)
        # return Response(serializer.data)
        return Response("Item Updated")
    
class OrderView(APIView):
    permission_classes = [IsAuthenticated]
    
    serializer_class = OrderItemsSerializer
    
    def get(self, request: Request):
        cart = Cart.objects.get(user=request.user)
        cartItems = CartItems.objects.filter(products=OuterRef('pk')).values('quantity')
        products_qs = Product.objects.order_by('id').annotate(quantities=Subquery(cartItems))
        products_prefetch = Prefetch('products', queryset=products_qs.only('id', 'name', 'price'))
        order = Order.objects.filter(cart_id=cart)
        if not order.exists():
            order = Order.objects.create(cart_id=cart, total=0)
            return Response({"order": OrderItemsSerializer(order).data})
        order = order.prefetch_related(products_prefetch).annotate(user=Value(request.user.email))
        serializer = OrderItemsSerializer(order, many=True)
        return Response(serializer.data)
    
    
    def post(self, request: Request):
        cart = Cart.objects.get(user=request.user)
        cartItems = cart.cartitems_set.all()
        total = 0
        order = Order.objects.filter(cart_id=cart).exists()
        if order:
            Order.objects.filter(cart_id=cart).get().products.clear()
        for cartItem in cartItems:
            order = Order.objects.filter(cart_id=cart).prefetch_related('products').get()
            order.products.add(cartItem.products, through_defaults={'quantity': cartItem.quantity})
            total += cartItem.products.price * cartItem.quantity
        order.total = total
        order.save()
        # cartItems.delete() when transaction is successful
        return Response("Order Created")
    
class TransactionView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request: Request,pk):
        order = Order.objects.get(pk=pk)
        user = request.user
        if order.paid:
            return Response("Order Already Paid")
        if user.balance < order.total:
            raise Error("Insufficient Balance")
        orderItems = OrderItems.objects.filter(order=order).values('products', 'quantity')
        with transaction.atomic():
            user.balance = F('balance') - order.total
            user.save()
            order.paid = True
            order.save()
            for product in orderItems:
                product_updated = Product.objects.select_for_update().get(pk=product['products'])
                product_updated.quantity = F('quantity') - product['quantity']
                product_updated.save()
            cart = Cart.objects.get(user=user)
            cart.products.clear()
        return Response("Transaction Successful")
    
    
    # def get(self, request: Request):
    #     order = Order.objects.filter(cart__user=request.user).get()
    #     return Response({"paid": order.paid})