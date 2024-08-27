from pprint import pprint

from django.db.models import F, OuterRef, Prefetch, Subquery
from django.shortcuts import render
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

import shop.models as models
import shop.serializers as serializers


# Create your views here.
class ProductListView(APIView):
    
    
    def get(self, request: Request):
        # return render(request, "shop/product_list.html")
        type_product = Prefetch('type_product_id', queryset=models.TypeProduct.objects.filter(name='Phone'))
        filter_product = models.ProductBrandType.objects.filter(brand_id__name="Apple")\
                                                        .prefetch_related(type_product)\
                                                        .values('product_id','brand_id__name')
        # print(filter_product)
        products = models.Product.objects.filter(id__in = Subquery(filter_product.values('product_id'))).annotate(brand=Subquery(filter_product.values('brand_id__name')[:1]))
        # products = products.annotate(brand=Subquery(OuterRef('type_product_id__brand_id__name')))
        serializer = serializers.ProductSerializer(products, many=True)
        return Response(serializer.data)
    
    
class ProductDetailView(APIView):
    
    
    def get(self, request: Request, pk):
        # type_product = models.TypeProduct.objects.filter(OuterRef('type_product_id'))
        product = models.Product.objects.filter(id=pk)
        product = product.annotate(brand=Subquery(product.values('type_product__brand__name')[:1]))
        # product = product.annotate(brand=Subquery(product.values('type_product__brand__name')[:1]))
        serializer = serializers.ProductSerializer(product, many=True) 
        return Response(serializer.data)
        return Response({"message":"ok"})