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
    
    path('category-delete/<int:pk>', CategoryDeleteView.as_view(), name='category-delete'),
    path('color-delete/<int:pk>', ColorDeleteView.as_view(), name='color-delete'),
    path('brand-delete/<int:pk>', BrandDeleteView.as_view(), name='brand-delete'),

    path('create/', ProductCreateView.as_view(), name='create'),
    path('list/', ProductListView.as_view(), name='list'),
    path('parent-list/', ParentProductListView.as_view(), name='parent-list'),

    path('detail/<int:id>', ProductDetailView.as_view(), name='detail'),
    path('update/<int:pk>', ProductUpdateView.as_view(), name='update'),
    path('delete/<int:pk>', ProductDeleteView.as_view(), name='delete'),
    
    path('variation-create/', ProductVariationCreateView.as_view(), name='variation-create'),
    path('variations/<int:id>', ProductVariationListView.as_view(), name='variations'),
    path('variation-detail/<int:pk>', VariationDetailView.as_view(), name='variation-detail'),
    path('variation-delete/<int:pk>', ProductVariationDeleteView.as_view(), name='variation-delete'),
    path('variation-update/<int:pk>', ProductVariationUpdateView.as_view(), name='variation-update'),
    path('variation-list/', VariationListView.as_view(), name='variation-list'),
    path('variation-spec/', SpecView.as_view(), name='variation-spec'),

    path('add-comment/', AddCommentView.as_view(), name='add-comment'),
    path('update-comment/<int:pk>', UpdateCommentView.as_view(), name='update-comment'),
    path('delete-comment/<int:id>', DeleteCommentView.as_view(), name='delete-comment'),

    path('statistics/products/', StatisticsProductsView.as_view(), name='statistics-products'),
    path('statistics/orders/number/', StatisticsOrderNumberView.as_view(), name='statistics-orders-number'),
    path('statistics/orders/money/', StatisticsOrderMoneyView.as_view(), name='statistics-orders-money'),

    path('slider/create/', SliderCreateView.as_view(), name='slider-create'),
    path('slider/list/', SliderListView.as_view(), name='slider-list'),
    path('slider/detail/<int:pk>', SliderDetailView.as_view(), name='slider-detail'),
    path('slider/nolist/', NotSliderListView.as_view(), name='slider-no-list'),
    path('slider/delete/<int:pk>', SliderDeleteView.as_view(), name='slider-delete'),
    path('slider/update/<int:pk>', SliderUpdateView.as_view(), name='slider-update'),

]

