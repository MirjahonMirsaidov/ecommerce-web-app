from django.contrib import admin

from .models import *


admin.site.register(Brand)
admin.site.register(Color)
admin.site.register(Category)
admin.site.register(Size)
admin.site.register(Product)
admin.site.register(ProductVariation)
admin.site.register(ProductImage)
