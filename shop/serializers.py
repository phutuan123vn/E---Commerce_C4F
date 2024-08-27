from rest_framework import serializers
import shop.models as models


class TypeProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TypeProduct
        fields = '__all__'
        
    def create(self, validated_data):
        return models.TypeProduct.objects.create(**validated_data)

class ProductSerializer(serializers.ModelSerializer):
    brand = serializers.CharField()
    
    class Meta:
        model = models.Product
        fields = ['id', 'name', 'price', 'description', 'created_at', 'updated_at', 'quantity', 'brand']
        # fields = "__all__"
        
    def create(self, validated_data):
        return models.Product.objects.create(**validated_data)
    
class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Brand
        fields = '__all__'
        
    def create(self, validated_data):
        return models.Brand.objects.create(**validated_data)