from django.contrib import admin

from .models import *


admin.site.register(Brand)
admin.site.register(Category)
admin.site.register(CategoryProduct)
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price", "product_code", "brand", "parent_id", "quantity", "is_import", "status")
admin.site.register(ProductAttributes)
admin.site.register(ProductImage)
admin.site.register(Slider)
