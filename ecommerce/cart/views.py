from django.http import HttpResponse
from rest_framework import generics, authentication, permissions, status
from rest_framework.mixins import UpdateModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView
from random import randint
from .models import *
from .serializers import *
from product.models import Product, ProductVariation

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

    return HttpResponse('Bajarildi')


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

            order = OrderBeta.objects.create(phone_number=phone_number, name=name)
            order.save()
            finish_price = 0
            for product_num in range(0, int(length)):
                product = request.data.get(f'product{product_num}')
                count = int(request.data.get(f'count{product_num}'))
                price = ProductVariation.objects.get(id=product).price
                single_overall_price = price*count
                finish_price += single_overall_price
                OrderProductBeta.objects.create(
                    order_id = order.id,
                    product_id=product,
                    count=count,
                    single_overall_price=single_overall_price,
                    price=price,
                    
                )
            print(finish_price)
            order.finish_price = finish_price
            order.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderStatisticsView(APIView):
    
    def get(self, request):
        finished_orders = OrderBeta.objects.filter(is_finished=True)
        finished_order = OrderBetaSerializer(finished_orders, many=True)
        return Response(finished_order)


class OrderBetaUpdateView(generics.GenericAPIView, UpdateModelMixin):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)
    queryset = OrderBeta.objects.all()
    serializer_class = OrderBetaSerializer

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class OrderProductBetaListView(generics.ListAPIView):
    serializer_class = OrderProductBetaListSerializer
    queryset = OrderProductBeta.objects.all()



class OrderBetaListView(generics.ListAPIView):
    serializer_class = OrderBetaSerializer
    queryset = OrderBeta.objects.all()


class OrderBetaDetailView(generics.RetrieveAPIView):
    serializer_class = OrderBetaSerializer
    
    def get_queryset(self):
        return OrderBeta.objects.all()


class OrderProductBetaDetailView(generics.RetrieveAPIView):
    serializer_class = OrderProductBetaListSerializer
    
    def get_queryset(self):
        return OrderProductBeta.objects.all()
        
      
        
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