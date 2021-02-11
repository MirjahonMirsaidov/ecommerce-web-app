from rest_framework import generics, authentication, permissions, status
from rest_framework.response import Response

from .models import *
from .serializers import *


class CartCreateView(generics.CreateAPIView):
    serializer_class = CartSerializer
    queryset = Cart.objects.all()
    authentication_classes = (authentication.TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )


class CartDetailView(generics.GenericAPIView):
    serializer_class = CartSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        carts = Cart.objects.filter(user=request.user.pk)
        for cart in carts:
            print(cart.user)
            return Response({'data': {'user':cart.user}})
