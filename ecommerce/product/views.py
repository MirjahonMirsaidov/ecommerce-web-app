import datetime
from django.http import JsonResponse, HttpResponse
import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import generics, permissions, authentication, status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import UpdateModelMixin
from rest_framework.views import APIView

from .models import *
from .serializers import *
from cart.models import OrderBeta


class CategoryCreateView(generics.CreateAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class CategoryListView(generics.ListAPIView):
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.filter(parent_id=0)


class CategoryChildListView(APIView):

    def get(self, request, id):
        categories = Category.objects.filter(parent_id=id)
        categories = CategorySerializer(categories, many=True)
        return Response(categories.data)


class CategoryDeleteView(generics.DestroyAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class CategoryDetailView(generics.RetrieveAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class CategoryUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class BrandCreateView(generics.CreateAPIView):
    serializer_class = BrandSerializer
    queryset = Brand.objects.all()


class BrandListView(generics.ListAPIView):
    serializer_class = BrandSerializer
    queryset = Brand.objects.all()


class BrandDeleteView(generics.DestroyAPIView):
    serializer_class = BrandSerializer
    queryset = Brand.objects.all()


class ProductCreateView(generics.CreateAPIView):
    serializer_class = ProductSerializer
    authentication_classes = (authentication.TokenAuthentication, )
    permission_classes = (permissions.IsAdminUser, )
    def post(self, request):
        try:
            serializer = ProductSerializer(data=request.data)
            name = request.data.get('name')
            description = request.data.get('description')
            brand = request.data.get('brand')
            is_import = request.data.get('is_import')
            price = request.data.get('price')
            parent_id = request.data.get('parent_id')
            quantity = request.data.get('quantity')
            product_code = request.data.get('product_code')
            leng = request.data.get('leng')
            if serializer.is_valid():
                product = serializer.save()
                for category_num in range(0, int(leng)):
                    category = request.data.get(f'category{category_num}')
                    CategoryProduct.objects.create(category_id=category, product_id=product.id)
                
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response("Error", status=status.HTTP_400_BAD_REQUEST)


class ProductListView(generics.ListAPIView):
    serializer_class = ProductGetSerializer
    queryset = Product.objects.all()


class ProductsByCategoryView(APIView):
    serializer_class = ProductGetSerializer
    def get(self, request, slug):
        category = Category.objects.get(slug=slug)
        
        categories = CategoryProduct.objects.filter(category_id=category.id)
        products = []
        for category in categories:
            product = Product.objects.get(id=category.product_id)
            products.append(product)
        products = ProductGetSerializer(products, many=True)
        return Response(products.data)


class ProductUpdateView(GenericAPIView, UpdateModelMixin):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class ProductDeleteView(generics.DestroyAPIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)
    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class ProductDetailView(generics.ListAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
#     def get(self, request, id):
#         available_sizes = []
#         available_colors = []
#         variations_list = []
#         product = Product.objects.get(id=id)
#         product_variations = ProductAttributes.objects.filter(parent_id=id)
#         for variation in product_variations:
#             if variation.size not in available_sizes:
#                 available_sizes.append(variation.size)
#             if variation.color not in available_colors:
#                 available_colors.append({'id': variation.color.id, 'name': variation.color.name})
#             imagesa = []
#             for image in ProductImage.objects.filter(product_id=variation.id):
#                 imagesa.append("http://127.0.0.1:8000" + image.images.url)

#             variations_list.append({
#                 "id": variation.id,
#             "parent_id": variation.parent_id,
#             "name": variation.name,
#             "description": variation.description,
#             "is_import": variation.is_import,
#             "created_at": variation.created_at,
#             "category": {
#                 "id": variation.category.id,
#                 "name": variation.category.name,
#                 "slug": variation.category.slug
#             },
#             "brand": {
#                 "id": variation.brand.id,
#                 "name": variation.brand.name,
#             },
#             "size": variation.size,
#             "color": {
#                 "id": variation.color.id,
#                 "name": variation.color.name,
#             },
#             "price": variation.price,
#             "variation_image": "http://127.0.0.1:8000" + variation.variation_image.url,
#             "quantity": variation.quantity,
#             "images": imagesa

#             })

#         return Response({
#             "id": 5,
#             "category": {
#                 "id": product.category.id,
#                 "name": product.category.name,
#                 "slug": product.category.slug
#             },
#             "brand": {
#                 "id": product.brand.id,
#                 "name": product.brand.name
#             },
#             "name": product.name,
#             "description": product.description,
#             'available_sizes': available_sizes,
#             'available_colors': available_colors,
#             "variations": variations_list
#         })


class ProductAttributesCreateView(generics.CreateAPIView):
    serializer_class = ProductAttributesSerializer
    queryset = ProductAttributes.objects.all()
    # authentication_classes = (authentication.TokenAuthentication, )
    # permission_classes = (permissions.IsAdminUser, )
    

class ProductAttributesListView(generics.ListAPIView):
    serializer_class = ProductAttributesSerializer
    queryset = ProductAttributes.objects.all()


class ProductAttributesDeleteView(generics.DestroyAPIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)
    serializer_class = ProductAttributesSerializer
    queryset = ProductAttributes.objects.all()


class ProductAttributesUpdateView(generics.GenericAPIView, UpdateModelMixin):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)
    queryset = ProductAttributes.objects.all()
    serializer_class = ProductAttributesSerializer

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

class VariationListView(generics.ListAPIView):
    serializer_class = ProductGetSerializer
    queryset = ProductAttributes.objects.all()
        

class VariationDetailView(generics.RetrieveAPIView):
    serializer_class = ProductGetSerializer
    queryset = ProductAttributes.objects.all()


class AddCommentView(generics.GenericAPIView):
    serializer_class = CommentSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        serializer = CommentSerializer(data=request.data)
        user = request.user
        product_id = request.data.get('product_id')
        message = request.data.get('message')
        point = request.data.get('point')
        print(product_id)
        if serializer.is_valid():
            comment_check = Comment.objects.filter(product_id=product_id, user_id=user.pk)
            if comment_check.exists():
                return Response('Yes')
            else:
                Comment.objects.create(product_id=product_id, user_id=user.pk, message=message, point=point)
            return Response('Okay')
        return Response('Serializer not valid')


class UpdateCommentView(generics.GenericAPIView):
    serializer_class = CommentSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def patch(self, request, pk):
        serializer = CommentSerializer(data=request.data)
        comment = Comment.objects.get(id=pk)
        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)


class DeleteCommentView(generics.GenericAPIView):
    serializer_class = CommentSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def delete(self, request, id):
        user_id = request.user.pk

        if id:
            comment = Comment.objects.get(id=id)
            if user_id == comment.user_id:
                comment.delete()
                return Response('Comment successfully deleted')
            else:
                return Response('You can only delete a comment you have written')
        else:
            return Response('Not found')


class StatisticsProductsView(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)
    serializer_class = StatisticsSerializer

    def post(self, request):
        days = int(request.data.get('date'))
        date1 = datetime.datetime.now() - datetime.timedelta(days)
        product_numbers = 0
        for product in Product.objects.all():
            date = datetime.datetime.strptime((str(product.created_at)[:10] + ' ' + str(product.created_at)[11:19]), '%Y-%m-%d %H:%M:%S')
            if date > date1:
                product_numbers += 1
        for product_variation in ProductAttributes.objects.all():
            date = datetime.datetime.strptime((str(product_variation.created_at)[:10] + ' ' + str(product_variation.created_at)[11:19]), '%Y-%m-%d %H:%M:%S')
            if date > date1:
                product_numbers +=1

        return Response({'number': product_numbers})


class StatisticsOrderNumberView(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)
    serializer_class = StatisticsSerializer

    def post(self, request):
        days = int(request.data.get('date'))
        date1 = datetime.datetime.now() - datetime.timedelta(days)
        order_numbers = 0
        for order in OrderBeta.objects.all():
            date = datetime.datetime.strptime((str(order.created_at)[:10] + ' ' + str(order.created_at)[11:19]),
                                              '%Y-%m-%d %H:%M:%S')
            if order.status == 'Tugallangan':
                if date > date1:
                    order_numbers += 1

        return Response({'number': order_numbers})


class StatisticsOrderMoneyView(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)
    serializer_class = StatisticsSerializer

    def post(self, request):
        days = int(request.data.get('date'))
        date1 = datetime.datetime.now() - datetime.timedelta(days)
        order_money = 0
        for order in OrderBeta.objects.all():
            date = datetime.datetime.strptime((str(order.created_at)[:10] + ' ' + str(order.created_at)[11:19]),
                                              '%Y-%m-%d %H:%M:%S')
            if order.status == 'Tugallangan':
                if date > date1:
                    orders = OrderBeta.objects.filter(created_at=order.created_at)
                    for order in orders:
                        order_money += order.finish_price

        return Response({'number': order_money})


class SliderCreateView(generics.CreateAPIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)
    serializer_class = SliderSerializer
    queryset = Slider.objects.all()


class SliderDeleteView(generics.DestroyAPIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)
    serializer_class = SliderSerializer
    queryset = Slider.objects.all()


class SliderDetailView(generics.RetrieveAPIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)
    serializer_class = SliderGetSerializer
    queryset = Slider.objects.all()


class SliderListView(generics.ListAPIView):
    serializer_class = SliderGetSerializer
    queryset = Slider.objects.filter(is_slider=True)


class NotSliderListView(generics.ListAPIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)
    serializer_class = SliderSerializer
    queryset = Slider.objects.filter(is_slider=False)


class SliderUpdateView(generics.GenericAPIView, UpdateModelMixin):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)
    serializer_class = SliderSerializer
    queryset = Slider.objects.all()

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
