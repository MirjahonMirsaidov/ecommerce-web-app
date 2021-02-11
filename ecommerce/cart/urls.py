from django.urls import path

from .views import *


app_name = 'cart'

urlpatterns = [
    path('create/', CartCreateView.as_view(), name='create'),
    path('list/', CartDetailView.as_view(), name='list'),
]