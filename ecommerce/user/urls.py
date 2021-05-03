from django.urls import path

from .views import *

app_name = 'user'


urlpatterns = [
    path('create/', UserApiView.as_view(), name='create'),
    path('token/', CreateTokenView.as_view(), name='token'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('me/', UserUpdateView.as_view(), name='me'),
    path('change_password/', ChangePasswordView.as_view(), name='auth_change_password'),
    path('list/', UserListView.as_view(), name='list'),
    path('profile-create/', ProfileCreateView.as_view(), name='profile-create'),
    path('address-create/', AddressCreateView.as_view(), name='address-create'),
]