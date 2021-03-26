from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, authentication, permissions, status, filters
from rest_framework.mixins import UpdateModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView
from random import randint
from .models import *
from .serializers import *
from product.models import Product, ProductAttributes

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


class CreateOrderBetaView(generics.GenericAPIView):
    serializer_class = OrderProductBetaSerializer

    def post(self, request):
        serializer = OrderProductBetaSerializer(data=request.data)
        leng = request.data.get('leng')
        name = request.data.get('name')
        phone_number = request.data.get('phone_number')
        order = OrderBeta.objects.get_or_create(phone_number=phone_number, name=name)[0]
        order.save()

        finish_price = 0
        try:
            for product_num in range(0, int(leng)):
                product = request.data.get(f'product{product_num}')
                if Product.objects.get(id=product).quantity > 0:
                    count = int(request.data.get(f'count{product_num}'))
                    price = Product.objects.get(id=product).price
                    product_code = Product.objects.get(id=product).product_code
                    single_overall_price = price * count
                    finish_price += single_overall_price
                    if serializer.is_valid():
                        
                        OrderProductBeta.objects.create(
                            order_id=order.id,
                            product_id=product,
                            count=count,
                            single_overall_price=single_overall_price,
                            price=price,
                            product_code=product_code,

                        )
                        order.finish_price = finish_price
                        order.save()
            
            # if not OrderProductBeta.objects.filter(order_id=order.id).exists():
            #     order.delete()
            return Response(status=status.HTTP_201_CREATED)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)



class OrderBetaListView(generics.ListAPIView):
    serializer_class = OrderBetaSerializer
    queryset = OrderBeta.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filter_fields = ['status', ]
    ordering_fields = ['created_at', ]
    search_fields = ['name', 'phone_number', ]


class OrderBetaDetailView(generics.RetrieveAPIView):
    serializer_class = OrderBetaSerializer
    
    def get_queryset(self):
        return OrderBeta.objects.all()


class OrderBetaUpdateView(generics.GenericAPIView, UpdateModelMixin):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)
    queryset = OrderBeta.objects.all()
    serializer_class = OrderBetaSerializer

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class OrderBetaDeleteView(generics.DestroyAPIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)
    queryset = OrderBeta.objects.all()
    serializer_class = OrderBetaSerializer


class OrderProductBetaUpdateView(generics.GenericAPIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)
    serializer_class = OrderProductBetaSerializer

    def post(self, request, pk):
        order_product = OrderProductBeta.objects.get(id=pk)
        count = int(request.data.get('count'))
        product_id = request.data.get('product')
        if product_id and count:
            product = Product.objects.get(id=product_id)
            price = product.price
            single_overall_price = price * count
            order_product.single_overall_price = single_overall_price
            order_product.product_id = product_id
            order_product.count = count
            order_product.save()
            order = OrderBeta.objects.get(id=order_product.order_id)
            order_products = OrderProductBeta.objects.filter(order_id=order.id)
            finish_price = 0
            for order_product in order_products:
                finish_price += order_product.single_overall_price
                order.finish_price = finish_price
                order.save()
            print(single_overall_price)
            return Response(order.finish_price, status=status.HTTP_200_OK)
        

class OrderProductBetaListView(generics.ListAPIView):
    serializer_class = OrderProductBetaListSerializer
    queryset = OrderProductBeta.objects.all()


class OrderProductBetaDeleteView(generics.DestroyAPIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)
    serializer_class = OrderProductBetaSerializer
    queryset = OrderProductBeta.objects.all()


class OrderProductBetaDetailView(generics.RetrieveAPIView):
    serializer_class = OrderProductBetaListSerializer
    
    def get_queryset(self):
        return OrderProductBeta.objects.all()
        
      
class ChangeStatusView(generics.GenericAPIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)
    def post(self, request, pk):
        status = request.data.get('status')
        order = OrderBeta.objects.get(id=pk)
        order.status=status
        order.save()

        if status == 'Tugallangan':
            order_products = OrderProductBeta.objects.filter(order_id=pk)
            ids = [order.product_id for order in order_products]
            for id in ids:
                product = ProductAttributes.objects.get(id=id)
                print(product.quantity)
                product.quantity -= 1
                product.save()
                print(product.quantity)

        return Response('Okay')

       
class BuyProductViaClickView(generics.GenericAPIView):
    serializer_class = BuySerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, url):
        url = ClickUz.generate_url(order_id='172', amount='150000', return_url='http://127.0.0.1:8000/api/cart/list/')
        print(url)
        return Response({'url': url})


# class OrderCheckAndPayment(ClickUz):
#     def check_order(self, order_id: str, amount: str):
#         return self.ORDER_FOUND


# class TestView(ClickUzMerchantAPIView):
#     VALIDATE_CLASS = OrderCheckAndPayment


# class CreateOrderView(generics.CreateAPIView):
#     serializer_class = OrderSerializer
#     authentication_classes = (authentication.TokenAuthentication,)
#     permission_classes = (permissions.IsAuthenticated,)

#     def successfully_payment(self, order_id: str, transaction: object):
#         print(order_id)


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