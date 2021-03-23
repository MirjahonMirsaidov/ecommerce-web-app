import datetime
from django.http import JsonResponse
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
    queryset = Category.objects.all()


class CategoryDeleteView(generics.DestroyAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class ColorCreateView(generics.CreateAPIView):
    serializer_class = ColorSerializer
    queryset = Color.objects.all()


class ColorListView(generics.ListAPIView):
    serializer_class = ColorSerializer
    queryset = Color.objects.all()


class ColorDeleteView(generics.DestroyAPIView):
    serializer_class = ColorSerializer
    queryset = Color.objects.all()


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
    queryset = Product.objects.all()
    authentication_classes = (authentication.TokenAuthentication, )
    permission_classes = (permissions.IsAdminUser, )


class ProductVariationCreateView(generics.GenericAPIView):
    serializer_class = ProductVariationSerializer
    authentication_classes = (authentication.TokenAuthentication, )
    permission_classes = (permissions.IsAdminUser, )


    def post(self, request):
        serializer = ProductVariationSerializer(data=request.data)
        leng = request.data.get('leng')
        parent = request.data.get('parent_id')
        size = request.data.get('size')
        color = request.data.get('color')
        price = request.data.get('price')
        variation_image = request.FILES.get('variation_image')
        quantity = request.data.get('quantity')
        name = Product.objects.get(id=parent).name
        brand = Product.objects.get(id=parent).brand
        category_id = Product.objects.get(id=parent).category_id
        description = Product.objects.get(id=parent).description
        is_import = Product.objects.get(id=parent).is_import

        if serializer.is_valid():
            check = ProductVariation.objects.filter(parent_id=parent, category_id=category_id, name=name, brand=brand, description=description, is_import=is_import, size=size, color_id=color).exists()
            if check:
                return Response("Variation alreadiy exist!", status=status.HTTP_409_CONFLICT)
            else:
                product = ProductVariation.objects.create(parent_id=parent, category_id=category_id, name=name, brand=brand, description=description, is_import=is_import, size=size, color_id=color, price=price, variation_image=variation_image, quantity=quantity, is_active=True)

                for file_num in range(0, int(leng)):
                    images = request.FILES.get(f'images{file_num}')
                    ProductImage.objects.create(
                        product=product,
                        images=images,
                    )
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VariationListView(generics.ListAPIView):
    serializer_class = ProductVariationGetSerializer
    queryset = ProductVariation.objects.filter(is_active=True, )
    size = django_filters.CharFilter(name='name')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filter_fields = ['is_import', 'parent', 'category', 'color', 'brand', 'size']
    search_fields = ['name', ]
    ordering_fields = ['price', 'name', 'created_at', ]


class SpecView(generics.GenericAPIView):
    
    def get(self, request):
        parent_id = request.GET.get('parent_id')
        color = request.GET.get('color')
        size = request.GET.get('size')
        
        products = ProductVariation.objects.filter(is_active=True, parent_id=parent_id, color=color, size=size)
        for product in products:
            return Response(product.id)
        

class VariationDetailView(generics.RetrieveAPIView):
    serializer_class = ProductVariationGetSerializer
    queryset = ProductVariation.objects.all()


class ProductVariationListView(generics.GenericAPIView):
    serializer_class = ProductVariationGetSerializer
    queryset = ProductVariation.objects.all()

    def get(self, request, id):
        products = ProductVariation.objects.filter(parent_id=id, is_active=True)
        serializer = ProductVariationGetSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductListView(generics.ListAPIView):
    serializer_class = ProductGetSerializer
    queryset = Product.objects.all()


class ParentProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class ProductDetailView(generics.RetrieveAPIView):
    serializer_class = ProductGetSerializer

    def get(self, request, id):
        available_sizes = []
        available_colors = []
        variations_list = []
        product = Product.objects.get(id=id)
        product_variations = ProductVariation.objects.filter(parent_id=id)
        for variation in product_variations:
            if variation.size not in available_sizes:
                available_sizes.append(variation.size)
            if variation.color not in available_colors:
                available_colors.append(variation.color.name)
            imagesa = []
            for image in ProductImage.objects.filter(product_id=variation.id):
                imagesa.append("http://127.0.0.1:8000" + image.images.url)

            variations_list.append({
                "id": variation.id,
            "parent_id": variation.parent_id,
            "name": variation.name,
            "description": variation.description,
            "is_import": variation.is_import,
            "created_at": variation.created_at,
            "category": {
                "id": variation.category.id,
                "name": variation.category.name,
                "slug": variation.category.slug
            },
            "brand": {
                "id": variation.brand.id,
                "name": variation.brand.name,
            },
            "size": variation.size,
            "color": {
                "id": variation.color.id,
                "name": variation.color.name,
            },
            "price": variation.price,
            "variation_image": "http://127.0.0.1:8000" + variation.variation_image.url,
            "quantity": variation.quantity,
            "images": imagesa

            })

        return Response({
            "id": 5,
            "category": {
                "id": product.category.id,
                "name": product.category.name,
                "slug": product.category.slug
            },
            "brand": {
                "id": product.brand.id,
                "name": product.brand.name
            },
            "name": product.name,
            "description": product.description,
            'available_sizes': available_sizes,
            'available_colors': available_colors,
            "variations": variations_list
        })


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


class ProductVariationDeleteView(generics.DestroyAPIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)
    serializer_class = ProductVariationSerializer
    queryset = ProductVariation.objects.all()


class ProductVariationUpdateView(generics.GenericAPIView, UpdateModelMixin):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)
    queryset = ProductVariation.objects.all()
    serializer_class = ProductVariationSerializer

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


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
        for product_variation in ProductVariation.objects.all():
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
