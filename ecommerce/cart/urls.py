from django.urls import path

from .views import *


app_name = 'cart'

urlpatterns = [
    path('create/', CartCreateView.as_view(), name='create'),
    path('list/', CartDetailView.as_view(), name='list'),
    path('add-to-cart/<int:id>', AddToCartProductView.as_view(), name='add-to-cart'),
    path('delete-from-cart/<int:id>', DeleteFromCartView.as_view(), name='delete-from-cart'),
    path('buy/', BuyProductViaClickView.as_view(), name='buy'),
    path('toggle-is-selected/<int:id>', toggle_is_selected_status, name='toggle-is-selected'),
    path('add-to-wishlist/<int:id>', AddWishListView.as_view(), name='add-to-wishlist'),

    path('orderbeta-create/', CreateOrderBetaView.as_view(), name='orderbeta-create'),
    path('orderbeta-list/', OrderBetaListView.as_view(), name='orderbeta-list'),
    path('orderbeta-detail/<int:pk>', OrderBetaDetailView.as_view(), name='orderbeta-detail'),
    path('orderbeta-update/<int:pk>', OrderBetaUpdateView.as_view(), name='orderbeta-update'),
    path('orderbeta-delete/<int:pk>', OrderBetaDeleteView.as_view(), name='orderbeta-delete'),
    path('change-status/<int:pk>', ChangeStatusView.as_view(), name='change-status'),

    path('orderproductbeta-list/', OrderProductBetaListView.as_view(), name='orderbeta-list'),
    path('orderproductbeta-create/', OrderProductBetaCreateView.as_view(), name='orderbeta-create'),
    path('orderproductbeta-update/<int:pk>', OrderProductBetaUpdateView.as_view(), name='orderproductbeta-update'),
    path('orderproductbeta-detail/<int:pk>', OrderProductBetaDetailView.as_view(), name='orderproductbeta-detail'),
    path('orderproductbeta-delete/<int:pk>', OrderProductBetaDeleteView.as_view(), name='orderproductbeta-delete'),

]