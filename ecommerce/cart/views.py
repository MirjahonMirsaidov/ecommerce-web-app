from rest_framework import generics, authentication, permissions, status
from rest_framework.response import Response
from .models import *
from .serializers import *
from product.models import Product


class CartCreateView(generics.CreateAPIView):
    serializer_class = CartSerializer
    queryset = Cart.objects.all()
    authentication_classes = (authentication.TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )


class CartDetailView(generics.ListAPIView):
    serializer_class = CartProductSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return CartProduct.objects.filter(user=user)


class OrderCreateView(generics.GenericAPIView):
    serializer_class = HistorySerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)


class AddToCartProductView(generics.GenericAPIView):
    serializer_class = CartProductSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, id):
        CartProduct.objects.get_or_create(user=request.user, product_id=id)
        return Response(status=status.HTTP_200_OK)

