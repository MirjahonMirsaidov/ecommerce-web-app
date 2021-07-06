from django.urls import path

from .views import *

app_name = 'user'


urlpatterns = [
    path('token/', CreateTokenView.as_view(), name='token'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('me/', UserUpdateView.as_view(), name='me'),
]