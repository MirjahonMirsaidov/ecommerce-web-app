from django.contrib import admin

from .models import *


admin.site.register(Cart)
admin.site.register(CartProduct)
admin.site.register(Order)
admin.site.register(OrderBeta)
admin.site.register(OrderProductBeta)