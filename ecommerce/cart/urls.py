from django.urls import path

from .views import *


app_name = 'cart'

urlpatterns = [
    path('create/', CartCreateView.as_view(), name='create'),
    path('list/', CartDetailView.as_view(), name='list'),
    path('add-to-cart/<int:id>', AddToCartProductView.as_view(), name='add-to-cart'),
    path('create-order/', CreateOrderView.as_view(), name='create-order'),
<<<<<<< HEAD
=======
    path('buy/', BuyProductViaClickView.as_view(), name='buy'),
    path('toggle-is-selected/<int:id>', toggle_is_selected_status, name='toggle-is-selected'),
>>>>>>> 922f6f5ed67ea4f481466718c1c877ed72d9ae89
]