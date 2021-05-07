from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, authentication, permissions, status, filters
from rest_framework.mixins import UpdateModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView
from random import randint
from .models import *
from .serializers import *
from .pagination import CustomPagination
from product.models import Product, ProductAttributes
import datetime

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
        return Response("Successfully deleted", status=status.HTTP_200_OK)


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
        name = request.data.get('name')
        phone_number = request.data.get('phone_number')
        products = request.data.get('products')
        
        if name and phone_number and products:
            order = OrderBeta.objects.create(phone_number=phone_number, name=name)
            order.save()

            finish_price = 0
            try:
                for prod in products:
                    product_id = prod['product_id']
                    count = int(prod['count'])
                    product = Product.objects.get(id=product_id)
                    if product.quantity > 0:
                        price = product.price
                        product_code = product.product_code
                        single_overall_price = price * count
                        finish_price += single_overall_price
                        if serializer.is_valid():

                            OrderProductBeta.objects.create(
                                order_id=order.id,
                                product_id=product.id,
                                count=count,
                                single_overall_price=single_overall_price,
                                price=price,
                                product_code=product_code,

                            )
                            order.finish_price = finish_price
                            order.save()

                    # if not OrderProductBeta.objects.filter(order_id=order.id).exists():
                    #     order.delete()
                return Response("Buyurtma muvaffaqiyatli qo'shildi", status=status.HTTP_201_CREATED)
            except:
                return Response(msg, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("Telefon raqam, ism va maxsulotlar bo'lishi shart!", status=status.HTTP_400_BAD_REQUEST)


class OrderBetaListView(generics.ListAPIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)
    serializer_class = OrderBetaSerializer
    pagination_class = CustomPagination
    CustomPagination.page_size = 10
    queryset = OrderBeta.objects.all().order_by('-id')
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filter_fields = ['status', ]
    ordering_fields = ['created_at', ]
    search_fields = ['name', 'phone_number', ]


class OrderBetaDetailView(generics.RetrieveAPIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)
    serializer_class = OrderBetaSerializer
    
    def get_queryset(self):
        return OrderBeta.objects.all()


class OrderBetaUpdateView(generics.GenericAPIView, UpdateModelMixin):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)
    queryset = OrderBeta.objects.all()
    serializer_class = OrderBetaSerializer

    def patch(self, request, *args, **kwargs):
        self.partial_update(request, *args, **kwargs)
        return Response("Buyurtma muvaffaqiyatli o'zgartirildi", status=status.HTTP_200_OK)
        

class OrderBetaDeleteView(generics.DestroyAPIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)
    queryset = OrderBeta.objects.all()
    serializer_class = OrderBetaSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance:
            self.perform_destroy(instance)
            return Response("Buyurtma muvaffaqiyatli o'chirildi", status=status.HTTP_204_NO_CONTENT)
        return Response("So'rovda xatolik mavjud", status=status.HTTP_400_BAD_REQUEST)



class OrderProductBetaUpdateView(generics.GenericAPIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)
    serializer_class = OrderProductBetaSerializer

    def patch(self, request, pk):
        try:
            order_product = OrderProductBeta.objects.get(id=pk)
            count = int(request.data.get('count'))
            if count:
                product_id = order_product.product_id
                product = Product.objects.get(id=product_id)
                price = product.price
                single_overall_price = price * count
                order_product.single_overall_price = single_overall_price
                order_product.count = count
                order_product.price = price
                order_product.save()
                order = OrderBeta.objects.get(id=order_product.order_id)
                order_products = OrderProductBeta.objects.filter(order_id=order.id)
                finish_price = 0
                for order_product in order_products:
                    finish_price += order_product.single_overall_price
                    order.finish_price = finish_price
                    order.save()
                return Response("Muvaffaqiyatli o'zgartirildi", status=status.HTTP_200_OK)
            else:
                return Response("Maxsulot sonini kiritmadingiz", status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response("Ma'lumotlar xato kiritilgan", status=status.HTTP_400_BAD_REQUEST)


class OrderProductBetaCreateView(generics.GenericAPIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)
    serializer_class = OrderProductBetaSerializer

    def post(self, request):
        try:
            order_id = request.data.get('order_id')
            product_id = request.data.get('product_id')
            count = int(request.data.get('count'))
            if product_id and count:
                if not OrderProductBeta.objects.filter(order_id=order_id, product_id=product_id).exists():
                    product = Product.objects.get(id=product_id)
                    price = product.price
                    single_overall_price = price * count
                    product_code = product.product_code
                    OrderProductBeta.objects.get_or_create(order_id=order_id, product_id=product_id, count=count, product_code=product_code, price=price, single_overall_price=single_overall_price)
                    order = OrderBeta.objects.get(id=order_id)
                    order.finish_price += single_overall_price
                    order.save()

                    return Response("Buyurtmaga maxsulot muvaffaqiyatli qo'shildi", status=status.HTTP_200_OK)
                else:
                    return Response("Bu maxsulot buyurtmada mavjud!", status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response("Maxsulot tanlanmagan yoki sonini kiritmadingiz", status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response("Ma'lumotlar xato kiritilgan", status=status.HTTP_400_BAD_REQUEST)


class OrderProductBetaListView(generics.ListAPIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)
    serializer_class = OrderProductBetaListSerializer
    queryset = OrderProductBeta.objects.all()


class OrderProductBetaDeleteView(generics.DestroyAPIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)
    serializer_class = OrderProductBetaSerializer
    queryset = OrderProductBeta.objects.all()

    def delete(self, request, id):
        try:
            orderproduct = OrderProductBeta.objects.get(id=id)
            order = OrderBeta.objects.get(id=orderproduct.order_id)
            orderproduct.delete()
            msg = "Buyurtmadagi maxsulot o'chirildi"
            if not OrderProductBeta.objects.filter(order=order.id).exists():
                order.delete()
                msg = "Buyurtmada maxsulot qolmadi. Buyurtma ham o'chiriladi"
            else:
                order.finish_price -= orderproduct.single_overall_price
                order.save()

            return Response(msg, status=status.HTTP_204_NO_CONTENT)
        except:
            return Response("So'rovda xatolik mavjud", status=status.HTTP_400_BAD_REQUEST)


class OrderProductBetaDetailView(generics.RetrieveAPIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)
    serializer_class = OrderProductBetaListSerializer
    
    def get_queryset(self):
        return OrderProductBeta.objects.all()
        
      
class ChangeStatusView(generics.GenericAPIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)
    serializer_class = OrderBetaSerializer
    def post(self, request, pk):
        try:
            status = request.data.get('status')
            order = OrderBeta.objects.get(id=pk)
            order.status=status
            order.save()

            if status == 'Tugallangan':
                order.created_at = datetime.datetime.now()
                order.save()
                order_products = OrderProductBeta.objects.filter(order_id=pk)
                ids = [order.product_id for order in order_products]
                for id in ids:
                    product = Product.objects.get(id=id)
                    product.quantity -= 1
                    product.save()

            return Response("Muvaffaqiyatli o'zgartirildi", status=status.HTTP_202_ACCEPTED)
        except:
            return Response("So'rovda xatolik mavjud", status=status.HTTP_400_BAD_REQUEST)

       
class BuyProductViaClickView(generics.GenericAPIView):
    serializer_class = BuySerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, url):
        url = ClickUz.generate_url(order_id='172', amount='150000', return_url='http://127.0.0.1:8000/api/cart/list/')
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
            return Response('Sahifa topilmadi', status=status.HTTP_404_NOT_FOUND)