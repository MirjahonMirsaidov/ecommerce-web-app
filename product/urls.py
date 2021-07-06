from django.urls import path, re_path

from .views import *

app_name = 'product'

urlpatterns = [
    path('category-create/', CategoryCreateView.as_view(), name='category-create'),
    path('category-list/', CategoryListView.as_view(), name='category-list'),
    path('category-all/', CategoryAllListView.as_view(), name='category-all'),
    path('category-delete/<int:id>', CategoryDeleteView.as_view(), name='category-delete'),
    path('category-detail/<int:pk>', CategoryDetailView.as_view(), name='category-detail'),
    path('category-childs/<int:id>', CategoryChildListView.as_view(), name='category-childs'),
    path('category-update/<int:pk>', CategoryUpdateView.as_view(), name='category-detail'),
    path('category-slider/', CategorySliderView.as_view(), name='category-slider'),

    path('brand-create/', BrandCreateView.as_view(), name='brand-create'),
    path('brand-list/', BrandListView.as_view(), name='brand-list'),
    path('brand-delete/<int:pk>', BrandDeleteView.as_view(), name='brand-delete'),

    path('create/', ProductCreateView.as_view(), name='create'),
    path('variation-create/', ProductVariationCreateView.as_view(), name='variation-create'),
    path('list/', ProductListView.as_view(), name='list'),

    re_path('by-category/(?P<slug>.+)/$', ProductsByCategoryView.as_view(), name='by-category'),

    path('detail/<int:id>', ProductDetailView.as_view(), name='detail'),
    path('update/<int:pk>', ProductUpdateView.as_view(), name='update'),
    path('delete/<int:pk>', ProductDeleteView.as_view(), name='delete'),
    path('specific/<int:id>', ProductSpecificDetailView.as_view(), name='specific'),

    path('attributes-list/', ProductAttributesListView.as_view(), name='attributes-list'),
    path('update-attributes/', ProductAttributesUpdateView.as_view(), name='attributes-update'),
    path('attributes-delete/<int:pk>', ProductAttributesDeleteView.as_view(), name='variation-delete'),
    path('update-category/', ProductCategoryUpdateView.as_view(), name='update-product-category'),
    path('update-images/', ProductImagesUpdateView.as_view(), name='update-product-images'),
    path('codesize/', CodeSizeListView.as_view(), name='codesize'),

    path('add-comment/', AddCommentView.as_view(), name='add-comment'),
    path('update-comment/<int:pk>', UpdateCommentView.as_view(), name='update-comment'),
    path('delete-comment/<int:id>', DeleteCommentView.as_view(), name='delete-comment'),

    path('statistics/products/', StatisticsProductsView.as_view(), name='statistics-products'),
    path('statistics/orders/number/', StatisticsOrderNumberView.as_view(), name='statistics-orders-number'),
    path('statistics/orders/money/', StatisticsOrderMoneyView.as_view(), name='statistics-orders-money'),

    path('slider/create/', SliderCreateView.as_view(), name='slider-create'),
    path('slider/list/', SliderListView.as_view(), name='slider-list'),
    path('slider/all/', SliderAllListView.as_view(), name='slider-all'),
    path('slider/detail/<int:pk>', SliderDetailView.as_view(), name='slider-detail'),
    path('slider/delete/<int:pk>', SliderDeleteView.as_view(), name='slider-delete'),
    path('slider/update/<int:pk>', SliderUpdateView.as_view(), name='slider-update'),

]

