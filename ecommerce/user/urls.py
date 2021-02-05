from django.urls import path

from .views import UserApiView, CreateTokenView, UserUpdateView


app_name = 'user'

urlpatterns = [
    path('create/', UserApiView.as_view(), name='create'),
    path('token/', CreateTokenView.as_view(), name='token'),
    path('me/', UserUpdateView.as_view(), name='me'),
]