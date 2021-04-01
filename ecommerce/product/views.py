import datetime
from django.http import JsonResponse, HttpResponse
import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins
from rest_framework import generics, permissions, authentication, status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import UpdateModelMixin
from rest_framework.views import APIView

from .models import *
from .serializers import *
from cart.models import OrderBeta
from utils.product import *


class CategoryCreateView(generics.CreateAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class CategoryAllListView(generics.ListAPIView):
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
    serializer_class = ProductCreateSerializer
    authentication_classes = (authentication.TokenAuthentication, )
    permission_classes = (permissions.IsAdminUser, )
    def post(self, request):
        # try:
        serializer = ProductCreateSerializer(data=request.data)
        name = request.data.get('name')
        description = request.data.get('description')
        brand = request.data.get('brand')
        is_import = request.data.get('is_import')
        price = request.data.get('price')
        parent_id = request.data.get('parent_id')
        quantity = request.data.get('quantity')
        image = request.data.get('image')
        product_code = request.data.get('product_code')
        categories = request.data.get('categories')
        attributes = request.data.get('attributes')
        images = request.data.get('images')
        print('working 119', type(images))
        variations = request.data.get('variations')
        if serializer.is_valid():
            print('working 122')

            product = Product.objects.create(
                name=name,
                description=description,
                brand_id=brand,
                is_import=is_import,
                price=price,
                parent_id=0,
                quantity=quantity,
                image=get_image_from_data_url(image)[0],
                product_code=product_code,
            )
            if categories:
                save_category(categories, product)

            if attributes:
                save_attribute(attributes, product)

            if images:
                save_image(images, product)

            if variations:
                print('working 134')
                for variation in variations:

                    var_product = Product.objects.create(
                        name=variation['name'],
                        description=variation['description'],
                        brand=product.brand,
                        is_import=product.is_import,
                        price=variation['price'],
                        parent_id=product.id,
                        quantity=variation['quantity'],
                        product_code=variation['product_code'],
                    )
                    if variation['image']:
                        print('yes')
                        img = get_image_from_data_url(variation['image'])[0],
                    else:
                        print('blank')
                        img = get_image_from_data_url(image)[0]
                    var_product.image = img
                    var_product.save()

                    var_categories = variation['categories']
                    if var_categories:
                        save_category(categories, var_product)
                    else:
                        save_category(categories, var_product)

                    attributes = variation['attributes']
                    if attributes:
                        save_attribute(attributes, var_product)

                    imagesa = variation['images']
                    if imagesa:
                        save_image(imagesa, var_product)
                    else:
                        save_image(images, var_product)


            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # except:
        #     return Response("Error", status=status.HTTP_400_BAD_REQUEST)


class ProductListView(generics.ListAPIView):
    serializer_class = ProductGetSerializer
    queryset = Product.objects.all()
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filter_fields = ['brand', 'parent_id', 'is_import']
    search_fields = ['name', 'product_code', ]
    ordering_fields = ['created_at', 'price']


class CodeSizeListView(APIView):

    def get(self, request):
        li = []
        for product in Product.objects.all():
            if ProductAttributes.objects.filter(product=product).exists():
                for attr in ProductAttributes.objects.filter(product=product):
                    if attr.key == 'size':
                        li.append({
                            "id": product.id,
                            "codesize": f'kod: {product.product_code}    o`lcham: {attr.value}'
                        })
        return Response(li)


class ProductsByCategoryView(generics.ListAPIView):
    serializer_class = ProductGetSerializer
    queryset = Product.objects.all()
    def get_queryset(self):
        slug = self.kwargs['slug']
        category = Category.objects.get(slug=slug)
        products = []
        if category.parent_id:
            categories = CategoryProduct.objects.filter(category_id=category.id)

            for category in categories:
                product = Product.objects.get(id=category.product_id)
                products.append(product)
        elif category.parent_id == 0:
            categories = Category.objects.filter(parent_id=category.id)
            for item in categories:
                singl = CategoryProduct.objects.filter(category_id=item.id)
                for iterr in singl:
                    product = Product.objects.get(id=iterr.product_id)
                    products.append(product)
        products = [product.id for product in products]

        return Product.objects.filter(id__in=products)

    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filter_fields = ['brand', 'parent_id', 'is_import']
    search_fields = ['name', ]
    ordering_fields = ['created_at', 'price']


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


class ProductDetailView(generics.GenericAPIView):
    serializer_class = ProductGetSerializer
    queryset = Product.objects.all()

    def get(self, request, id):
        variations_list = []
        product = Product.objects.get(id=id)
        child = Product.objects.get(id=id)
        if product.parent_id:
            id = product.parent_id
            product = Product.objects.get(id=id)
        product_variations = Product.objects.filter(parent_id=id)

        # getting product childs
        for variation in product_variations:

            variations_list.append({
            "id": variation.id,
            "parent_id": variation.parent_id,
            "name": variation.name,
            "description": variation.description,
            "product_code": variation.product_code,
            "is_import": variation.is_import,
            "brand": {
                "id": variation.brand.id,
                "name": variation.brand.name,
            },
            "categories": get_categories(variation),
            "attributes": get_attributes(variation.id),
            "price": variation.price,
            "image": "http://127.0.0.1:8000" + variation.image.url,
            "quantity": variation.quantity,
            "images": get_images(variation),
            "created_at": variation.created_at,

            })
        return Response({
            "id": product.id,
            "parent_id": product.parent_id,
            "name": product.name,
            "description": product.description,
            "product_code": product.product_code,
            "is_import": product.is_import,
            "brand": {
                "id": product.brand.id,
                "name": product.brand.name,
            },
            "categories": get_categories(product),
            "attributes": get_attributes(id),
            "price": product.price,
            "image": "http://127.0.0.1:8000" + product.image.url,
            "quantity": product.quantity,
            "images": get_images(product),
            "slider_images": get_images(child),
            "created_at": product.created_at,
            "available_colors": get_available_colors_and_sizes(id)[0],
            "available_sizes": get_available_colors_and_sizes(id)[1],
            "variations": variations_list,
        })


class ProductAttributesListView(generics.ListAPIView):
    serializer_class = ProductAttributesSerializer
    queryset = ProductAttributes.objects.all()


class ProductAttributesDeleteView(generics.DestroyAPIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)
    serializer_class = ProductAttributesSerializer
    queryset = ProductAttributes.objects.all()


class ProductAttributesUpdateView(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)

    def post(self, request):
        # try:
            attributes = request.data.get('attributes')
            product = int(request.data.get('product'))
            if attributes:
                for item in ProductAttributes.objects.filter(product_id=product):
                        if item.id not in [atr.get('id') for atr in attributes]:
                            item.delete()

                for attr in attributes:
                    attr['product'] = product
                    if attr['id']:
                        attribut = ProductAttributes.objects.get(id=attr['id'])
                        serializer = ProductAttributesSerializer(attribut, data=attr)

                    else:
                        serializer = ProductAttributesSerializer(data=attr)

                    if serializer.is_valid():
                        serializer.save()



                return Response(status=status.HTTP_200_OK)
            return Response(status=status.HTTP_404_NOT_FOUND)
        # except:
        #     return Response(status=status.HTTP_400_BAD_REQUEST)


class ProductImagesUpdateView(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)

    def post(self, request):
        product = int(request.data.get('product'))
        images = request.data.get('images')
        for image in ProductImage.objects.filter(product_id=product):
            if image.images not in [img.split('media/')[-1] for img in images]:
                image.delete()
        for image in images:
            image = image.split('media/')[-1]
            if not ProductImage.objects.filter(product_id=product, images=image).exists():
                ProductImage.objects.create(
                    product_id=product,
                    images=get_image_from_data_url(image)[0],
                )
        return Response(status=status.HTTP_200_OK)


class ProductCategoryUpdateView(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)

    def post(self, request):
        product = request.data.get('product')
        categories_list = request.data.get('categories')
        for item in CategoryProduct.objects.filter(product_id=product):
            if item.category_id not in categories_list:
                item.delete()
        for category in categories_list:
            CategoryProduct.objects.get_or_create(category_id=category,
                                                 product_id=product)

        return Response(status=status.HTTP_200_OK)


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
