from django.urls import path

from .views import *

app_name = 'product'

urlpatterns = [
    path('category-create/', CategoryCreateView.as_view(), name='category-create'),
    path('color-create/', ColorCreateView.as_view(), name='color-create'),
    path('brand-create/', BrandCreateView.as_view(), name='brand-create'),

    path('category-list/', CategoryListView.as_view(), name='category-list'),
    path('color-list/', ColorListView.as_view(), name='color-list'),
    path('brand-list/', BrandListView.as_view(), name='brand-list'),
    
    path('create/', ProductCreateView.as_view(), name='create'),
    path('list/', ProductListView.as_view(), name='list'),
    path('detail/<int:pk>', ProductDetailView.as_view(), name='detail'),
    path('update/<int:pk>', ProductUpdateView.as_view(), name='update'),
    path('delete/<int:pk>', ProductDeleteView.as_view(), name='delete'),
    
    path('variation-create/', ProductVariationCreateView.as_view(), name='variation-create'),
    path('variations/<int:id>', ProductVariationListView.as_view(), name='variations'),
    path('variation-detail/<int:pk>', VariationDetailView.as_view(), name='variation-detail'),
    path('variation-list/', VariationListView.as_view(), name='variation-list'),
    path('variation-by-category/<slug:slug>', ProductVariationByCategory.as_view(), name='variation-list'),
    
    path('imported/', ImportedProductsView.as_view(), name='imported'),
    path('local/', LocalProductsView.as_view(), name='local'),

    path('add-comment/', AddCommentView.as_view(), name='add-comment'),
    path('update-comment/<int:pk>', UpdateCommentView.as_view(), name='update-comment'),
    path('delete-comment/<int:id>', DeleteCommentView.as_view(), name='delete-comment'),
]