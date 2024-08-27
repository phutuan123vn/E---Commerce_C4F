from django.urls import path
from shop import views
from rest_framework import routers

urlpatterns = [
    path("products/", views.ProductListView.as_view(), name="product_list"),
    path("products/<int:pk>/", views.ProductDetailView.as_view(), name="product_detail"),
]