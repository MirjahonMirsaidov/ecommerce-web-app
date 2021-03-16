from django.urls import path

from .views import *

app_name = 'product'

urlpatterns = [
    path('category-create/', CategoryCreateView.as_view(), name='category-create'),
    path('color-create/', ColorCreateView.as_view(), name='color-create'),
    path('brand-create/', BrandCreateView.as_view(), name='brand-create'),
    path('create/', ProductCreateView.as_view(), name='create'),
    path('variation-create/', ProductVariationCreateView.as_view(), name='variation-create'),
    path('list/', ProductListView.as_view(), name='list'),
    path('detail/<int:pk>', ProductDetailView.as_view(), name='detail'),
    path('update/<int:pk>', ProductUpdateView.as_view(), name='update'),
    path('variation-list/<int:id>', ProductVariationListView.as_view(), name='variation-list'),
    path('delete/<int:pk>', ProductDeleteView.as_view(), name='delete'),
    path('imported/', ImportedProductsView.as_view(), name='imported'),
    path('local/', LocalProductsView.as_view(), name='local'),
    path('by-category/<slug:slug>', ProductByCategoryView.as_view()),
    path('add-comment/', AddCommentView.as_view(), name='add-comment'),
    path('update-comment/<int:pk>', UpdateCommentView.as_view(), name='update-comment'),
    path('delete-comment/<int:id>', DeleteCommentView.as_view(), name='delete-comment'),


]