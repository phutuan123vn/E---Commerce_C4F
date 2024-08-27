from rest_framework import serializers

from inventory.models import Cart, CartItems, Product, Order


class ProductSerializer(serializers.ModelSerializer):
    quantities = serializers.IntegerField(default=0, read_only=True)
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'quantities']


class CartSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.email', read_only=True)
    products = ProductSerializer(many=True, read_only=True)
    total = serializers.CharField(default=0, read_only=True)
    product_id = serializers.IntegerField(write_only=True)
    quantity = serializers.IntegerField(write_only=True)
    class Meta:
        model = Cart
        fields = ['id', 'user', 'products',
                  'total','product_id','quantity'
                  ]
        
    def to_representation(self, instance):
        products = instance.products.all()
        total = 0
        for product in products:
            total += product.price * product.quantities
        ret = super().to_representation(instance)
        ret['total'] = f"{total:,}"
        return ret
    
    
class OrderItemsSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)
    # total = serializers.CharField(default=0, read_only=True)
    user = serializers.CharField(source='cart_id.user',read_only=True)
    cart = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Order
        fields = ['id', 'user', 'products', 'cart','total','paid','created_at','updated_at']
        
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        # ret['total'] = f"{ret['total']:,}"
        return ret

# class CartItemSerializer(serializers.ModelSerializer):
#     cart = CartSerializer(source='cart')
#     class Meta:
#         model = CartItem
#         fields = '__all__'
