from django.http import HttpResponse
from rest_framework import generics, authentication, permissions, status
from rest_framework.response import Response
from random import randint
from .models import *
from .serializers import *
from product.models import Product
from twilio.rest import Client

from clickuz import ClickUz
from clickuz.views import ClickUzMerchantAPIView


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



class AddToCartProductView(generics.GenericAPIView):
    serializer_class = CartProductSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)


    def post(self, request, id):
        serializer = CartProductSerializer(data=request.data)

        if serializer.is_valid():
            count = serializer.data.get('count')
            CartProduct.objects.get_or_create(user=request.user, product_id=id, count=count)
            return Response(status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteFromCartView(generics.GenericAPIView):
    serializer_class = CartProductSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)


    def delete(self, request, id):
        product = CartProduct.objects.get(id=id)
        product.delete()
        return Response("Successfully deleted")



def toggle_is_selected_status(request, id):
    cart_product = CartProduct.objects.get_or_create(id=id)
    status = cart_product[0].is_selected
    if status:
        cart_product[0].is_selected = False
    else:
        cart_product[0].is_selected = True
    cart_product[0].save()
<<<<<<< HEAD
    return HttpResponse('Bajarildi')
=======
    return HttpResponse('')
>>>>>>> 8c607df2e673605b9e213c7447af35df9817a42b


class CreateOrderView(generics.GenericAPIView):
    serializer_class = OrderSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        serializer = OrderSerializer(data=request.data)

        if serializer.is_valid():
            overall_price = serializer.data.get('overall_price')
            is_paid = serializer.data.get('is_paid')
            Order.objects.create(user=request.user, overall_price=overall_price, is_paid=is_paid)
            return Response(status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_400_BAD_REQUEST)



class CreateOrderProductBetaView(generics.GenericAPIView):
    serializer_class = OrderProductBetaSerializer


    def post(self, request):
        serializer = OrderProductBetaSerializer(data=request.data)
        length = request.data.get('length')
        name = request.data.get('name')
        phone_number = request.data.get('phone_number')
        if serializer.is_valid():
            for product_num in range(0, int(length)):
                product = request.data.get(f'product{product_num}')
                count = int(request.data.get(f'count{product_num}'))
                price = Product.objects.get(id=product).price
                overall_price = price*count
                print(overall_price)
                OrderProductBeta.objects.create(
                    product_id=product,
                    count=count,
                    phone_number=phone_number,
                    overall_price=overall_price,
                    name=name,
                )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class OrderProductBetaListView(generics.ListAPIView):
    serializer_class = OrderProductBetaListSerializer
    queryset = OrderProductBeta.objects.all()




class BuyProductViaClickView(generics.GenericAPIView):
    serializer_class = BuySerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, url):
        url = ClickUz.generate_url(order_id='172', amount='150000', return_url='http://127.0.0.1:8000/api/cart/list/')
        print(url)
        return Response({'url': url})



class OrderCheckAndPayment(ClickUz):
    def check_order(self, order_id: str, amount: str):
        return self.ORDER_FOUND



class TestView(ClickUzMerchantAPIView):
    VALIDATE_CLASS = OrderCheckAndPayment


class CreateOrderView(generics.CreateAPIView):
    serializer_class = OrderSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def successfully_payment(self, order_id: str, transaction: object):
        print(order_id)


class AddWishListView(generics.GenericAPIView):
    serializer_class = WishListSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, id):
        if id:   
            user_id = request.user.pk
            wished = WishList.objects.filter(user_id=user_id, product_id=id)
            if wished:
                wished.delete()
                return Response("Product successfully deleted from  WishList")
            else:
                WishList.objects.create(user_id=user_id, product_id=id)
                return Response("Product successfully added to WishList")
        else:
            return Response('Sahifa topilmadi')