from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=0)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # type_product = models.ForeignKey('TypeProduct', on_delete=models.CASCADE)
    type_product = models.ManyToManyField('TypeProduct', through='ProductBrandType')
    quantity = models.PositiveIntegerField(default=10)
    
    
    def __str__(self):
        return f"{self.name} - {self.price} - {self.type_product.all()}"
    
    
class Brand(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name
    
    
    
class TypeProduct(models.Model):
    name = models.CharField(max_length=255)
    brand = models.ManyToManyField(Brand, through='ProductBrandType')
    
    def __str__(self):
        return self.name
    

class ProductBrandType(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    brand_id = models.ForeignKey(Brand, on_delete=models.CASCADE)
    type_product_id = models.ForeignKey(TypeProduct, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Product: {self.product_id.name} - Brand: {self.brand_id.name} - Type: {self.type_product_id.name}"