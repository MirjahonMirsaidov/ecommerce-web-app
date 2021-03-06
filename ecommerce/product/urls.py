from django.urls import path

from .views import *

app_name = 'product'

urlpatterns = [
    path('category-create/', CategoryCreateView.as_view(), name='category-create'),
    path('color-create/', ColorCreateView.as_view(), name='color-create'),
    path('brand-create/', BrandCreateView.as_view(), name='brand-create'),
    path('size-create/', SizeCreateView.as_view(), name='size-create'),
    path('product-create/', ProductCreateView.as_view(), name='product-create'),
    path('product-list/', ProductListView.as_view(), name='product-list'),
    path('product-update/<int:pk>', ProductUpdateView.as_view(), name='product-update'),
    path('product-delete/<int:pk>', ProductDeleteView.as_view(), name='product-delete'),
    path('imported/', ImportedProductsView.as_view(), name='imported'),
    path('local/', LocalProductsView.as_view(), name='local'),
    path('by-category/<slug:slug>', ProductByCategoryView.as_view()),

]