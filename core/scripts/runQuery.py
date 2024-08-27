from pprint import pprint
from shop.models import Product, Brand, TypeProduct, ProductBrandType
from django.db.models import Q, OuterRef, Subquery, Sum,Value, CharField, Prefetch, F, IntegerField
from rest_framework_simplejwt.tokens import RefreshToken
from core.models import User
from shop.models import Product, Brand, TypeProduct, ProductBrandType
import inventory.models as IventoryModels

def run():
    # query = TypeProduct.objects.all()
    # print(query)
    # print(query[0].brand.all())
    user = User.objects.get(id=2)
    products_prefetch = Prefetch('products', queryset=Product.objects.order_by('id').only('id', 'name', 'price'))
    cart = IventoryModels.Cart.objects.filter(user=user).prefetch_related(products_prefetch)\
        .only('id', 'user', 'products').annotate(totoal=Sum(F('products__price') * F('cartitems__quantity'), output_field=IntegerField()))
    
    
    print(cart.values())