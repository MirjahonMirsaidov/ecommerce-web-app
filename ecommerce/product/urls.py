from django.urls import path

from .views import *

app_name = 'product'

urlpatterns = [
    path('category-create/', CategoryCreateView.as_view(), name='category-create'),
    path('color-create/', ColorCreateView.as_view(), name='color-create'),
    path('brand-create/', BrandCreateView.as_view(), name='brand-create'),
    path('size-create/', SizeCreateView.as_view(), name='size-create'),
    path('product-create/', ProductCreateView.as_view(), name='product-create'),
]