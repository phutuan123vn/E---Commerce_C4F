from django.urls import path
from inventory import views
# Define the URL patterns for the inventory app

urlpatterns = [
    path("carts/", views.CartItemView.as_view(), name="cart-items"),
    path("order/", views.OrderView.as_view(), name="order"), 
    path("order/<uuid:order_id>/", views.TransactionView.as_view(), name="order-transaction"),
]