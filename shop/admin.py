from django.contrib import admin
from core.admin import AdminUser
import shop.models as model
# Register your models here.


@admin.register(model.Product)
class AdminProduct(admin.ModelAdmin):
    pass

@admin.register(model.Brand)
class AdminBrand(admin.ModelAdmin):
    pass

@admin.register(model.TypeProduct)
class AdminTypeProduct(admin.ModelAdmin):
    pass

@admin.register(model.ProductBrandType)
class AdminProductBrandType(admin.ModelAdmin):
    pass