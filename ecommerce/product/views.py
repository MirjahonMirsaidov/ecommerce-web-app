import datetime
import os
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins
from rest_framework import generics, permissions, authentication, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import UpdateModelMixin
from rest_framework.views import APIView
from django.core.files.storage import default_storage

from .models import *
from .serializers import *
from cart.models import OrderBeta
from utils.product import *
from .pagination import CustomPagination


class CategoryCreateView(generics.CreateAPIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class CategoryAllListView(generics.ListAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class CategoryListView(generics.GenericAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    def get(self, request):
        parents = []
        parent_categories = Category.objects.filter(parent_id=0)
        for pc in parent_categories:
            childs = []
            for child in Category.objects.filter(parent_id=pc.id):
                childs.append({
                    "id": child.id,
                    "parent_id": child.parent_id,
                    "name": child.name,
                    "is_slider": child.is_slider,
                    "slug": child.slug,
                })
            parents.append({
                "id": pc.id,
                "name": pc.name,
                "is_slider": pc.is_slider,
                "slug": pc.slug,
                "childs": childs,
            })
        return Response(parents)


class CategoryChildListView(APIView):

    def get(self, request, id):
        categories = Category.objects.filter(parent_id=id)
        categories = CategorySerializer(categories, many=True)
        return Response(categories.data)


class CategoryDeleteView(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)

    def delete(self, request, id):
        if (not Category.objects.get(id=id).is_slider == True) or Category.objects.filter(is_slider=True).count() > 3:
            for category in Category.objects.filter(Q(id=id) | Q(parent_id=id)):
                category.delete()
            for item in CategoryProduct.objects.filter(category_id=id):
                item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("O'chirib bo'lmaydi")


class CategoryDetailView(generics.RetrieveAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class CategoryUpdateView(generics.GenericAPIView, UpdateModelMixin):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)
    serializer_class = CategorySerializer
    queryset = CategorySerializer

    def patch(self, request, pk):
        try:
            sliders = Category.objects.filter(is_slider=True).count()
            is_slider = request.data.get('is_slider').capitalize()
            category = Category.objects.get(id=pk)
            if sliders <= 3 and is_slider=='False':
                is_slider = True
                msg = "Slayderga eng kamida 3 ta kategoriya chiqishi kerak"
            else:
                msg = "Muvaffaqiyatli o'zgartirildi"  
            category.name = request.data.get('name')
            category.is_slider = is_slider
            if request.data.get('image'):
                category.image = request.data.get('image')
            category.order = request.data.get('order')
            category.parent_id = request.data.get('parent_id')
            category.updated_at = datetime.datetime.now()
            category.save()
            return Response(msg, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class CategorySliderView(generics.ListAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.filter(is_slider=True).order_by('-updated_at')[:3]


class BrandCreateView(generics.CreateAPIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)
    serializer_class = BrandSerializer
    queryset = Brand.objects.all()


class BrandListView(generics.ListAPIView):
    serializer_class = BrandSerializer
    queryset = Brand.objects.all()


class BrandDeleteView(generics.DestroyAPIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)
    serializer_class = BrandSerializer
    queryset = Brand.objects.all()


class ProductCreateView(generics.CreateAPIView):
    serializer_class = ProductCreateSerializer
    authentication_classes = (authentication.TokenAuthentication, )
    permission_classes = (permissions.IsAdminUser, )

    def post(self, request):
        try:
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
            variations = request.data.get('variations')
            if serializer.is_valid():
                if len(images) < 6:
                    if not check_product_exists(product_code, attributes):
                        if get_image_from_data_url(image):

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

                            try:
                                if variations:
                                    for variation in variations:
                                        if variation['image']:
                                            image = variation['image']
                                        if not check_product_exists(variation['product_code'], variation['attributes']):
                                            if get_image_from_data_url(image):

                                                var_product = Product.objects.create(
                                                    name=variation['name'],
                                                    description=variation['description'],
                                                    brand=product.brand,
                                                    is_import=product.is_import,
                                                    price=variation['price'],
                                                    parent_id=product.id,
                                                    image=get_image_from_data_url(image)[0],
                                                    quantity=variation['quantity'],
                                                    product_code=variation['product_code'],
                                                )


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
                                            else:
                                                return Response("png, jpg, jpeg, webp, Rasm kiriting", status=status.HTTP_400_BAD_REQUEST)

                            except:
                                return Response("Produkt variatsiyalarda xatolik bor")

                            return Response(serializer.data, status=status.HTTP_200_OK)
                        return Response("png, jpg, jpeg, webp, Rasm kiriting", status=status.HTTP_400_BAD_REQUEST)
                    else:
                        return Response("Bu maxsulot allaqachon yaratilgan!", status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response("Rasmlar soni 5 dan ko'p bolishi mumkin emas")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response("Error", status=status.HTTP_400_BAD_REQUEST)


class ProductVariationCreateView(generics.GenericAPIView):
    serializer_class = ProductCreateSerializer
    authentication_classes = (authentication.TokenAuthentication, )
    permission_classes = (permissions.IsAdminUser, )

    def post(self, request):
        try:
            parent_id = request.data.get('parent_id')
            name = request.data.get('name')
            description = request.data.get('description')
            price = request.data.get('price')
            quantity = request.data.get('quantity')
            product_code = request.data.get('product_code')
            categories = request.data.get('categories')
            attributes = request.data.get('attributes')
            image = request.data.get('image')
            images = request.data.get('images')
            product = Product.objects.get(id=parent_id)

            if not image:
                image = product.image
            if len(images) < 9:
                if not check_product_exists(product_code, attributes):
                    var_product = Product.objects.create(
                        name=name,
                        description=description,
                        brand=product.brand,
                        is_import=product.is_import,
                        price=price,
                        parent_id=product.id,
                        image=get_image_from_data_url(image)[0],
                        quantity=quantity,
                        product_code=product_code,
                        )
                    save_attribute(attributes, var_product)
                    save_category(categories, var_product)
                    if images:
                        save_image(images, var_product)
                    else:
                        images = ProductImage.objects.filter(product_id=parent_id)
                        save_image(images, var_product)
                    return Response(status=status.HTTP_200_OK)
                else:
                    return Response("Bu maxsulot variatsiya allaqachon yaratilgan")
            else:
                return Response("Rasmlar soni 8tadan ko'p bolishi mumkin emas")
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class ProductListView(generics.ListAPIView):
    serializer_class = ProductGetSerializer
    # queryset = Product.objects.all()
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filter_fields = ['brand', 'parent_id', 'is_import']
    search_fields = ['name', 'product_code', ]
    ordering_fields = ['created_at', 'price']
    pagination_class = CustomPagination
    CustomPagination.page_size = 10

    def get_queryset(self):
        return Product.objects.select_related('brand', )


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
            categories = CategoryProduct.objects.filter(category_id=category.id).values('product_id')

            for category in categories:
                product = Product.objects.get(id=category.get('product_id')).id
                products.append(product)
        else:
            categories = Category.objects.filter(Q(parent_id=category.id) | Q(id=category.id)).values('id')
            for item in categories:
                singl = CategoryProduct.objects.filter(category_id=item.get('id'))
                for iterr in singl:
                    product = Product.objects.get(id=iterr.product_id).id
                    products.append(product)

        return Product.objects.filter(id__in=products).select_related('brand')

    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filter_fields = ['brand', 'parent_id', 'is_import']
    search_fields = ['name', ]
    ordering_fields = ['created_at', 'price']
    pagination_class = CustomPagination
    CustomPagination.page_size = 10


class ProductUpdateView(GenericAPIView, UpdateModelMixin):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class ProductDeleteView(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)

    def delete(self, request, pk):
        product = Product.objects.get(pk=pk)
        product.delete()
        for item in CategoryProduct.objects.filter(product_id=pk):
            item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductDetailView(generics.GenericAPIView):
    serializer_class = ProductGetSerializer
    queryset = Product.objects.all()

    def get(self, request, id):
        variations_list = []
        product = Product.objects.get(id=id)
        child = product
        if product.parent_id:
            id = product.parent_id
            product = Product.objects.get(id=id)
        product_variations = Product.objects.filter(parent_id=id).select_related('brand')

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
                "id": variation.brand_id,
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
            "variations": variations_list,
        })


class ProductSpecificDetailView(generics.GenericAPIView):
    serializer_class = ProductGetSerializer
    queryset = Product.objects.all()

    def get(self, request, id):
        product = Product.objects.get(id=id)

        return Response({
            "id": product.id,
            "name": product.name,
            "product_code": product.product_code,
            "brand": {
                "id": product.brand.id,
                "name": product.brand.name,
            },
            "categories": get_categories(product),
            "attributes": get_attributes(id),
            "price": product.price,
            "quantity": product.quantity,
            "image": "http://127.0.0.1:8000" + product.image.url,
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
        try:
            attributes = request.data.get('attributes')
            product = int(request.data.get('product'))
            if attributes:
                for item in ProductAttributes.objects.filter(product_id=product):
                        if item.id not in [atr.get('id') for atr in attributes]:
                            item.delete()

                for attr in attributes:
                    attr['product'] = product
                    if attr.get('id'):
                        attribut = ProductAttributes.objects.get(id=attr.get('id'))
                        serializer = ProductAttributesSerializer(attribut, data=attr)
                    else:
                        serializer = ProductAttributesSerializer(data=attr)

                    if serializer.is_valid():
                        serializer.save()



                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(status=status.HTTP_404_NOT_FOUND)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class ProductImagesUpdateView(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)

    def post(self, request):
        try:
            product = int(request.data.get('product'))
            images = request.data.get('images')
            deleted_images = request.data.get('deleted_images')
            if deleted_images:
                for image in deleted_images:
                    img = image.split('media/')[1]
                    print(default_storage.delete(img))
                    image = ProductImage.objects.filter(product_id=product, images=img)
                    image.delete()
                    try:
                        os.remove(img)
                        print("% s removed successfully" % img)
                    except:
                        print("File path can not be removed")
                    # os.remove('http://127.0.0.1:8000/media/' + img)
            if images:
                for image in images:
                        ProductImage.objects.create(
                            product_id=product,
                            images=get_image_from_data_url(image)[0],
                        )
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class ProductCategoryUpdateView(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)

    def post(self, request):
        try:
            product = request.data.get('product')
            categories_list = request.data.get('categories')
            if categories_list:
                category_products = CategoryProduct.objects.filter(product_id=product)
                for item in category_products:
                    if item.category_id not in categories_list:
                        item.delete()
                for category in categories_list:
                    CategoryProduct.objects.get_or_create(category_id=category,
                                                         product_id=product)

                return Response(status=status.HTTP_200_OK)
            else:
                return Response("Mahsulotda kamida 1ta kategoriya bolishi kerak")
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class StatisticsProductsView(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)
    serializer_class = StatisticsSerializer

    def post(self, request):
        try:
            days = int(request.data.get('date'))
            date1 = datetime.datetime.now() - datetime.timedelta(days)
            product_numbers = 0
            for product in Product.objects.all():
                date = datetime.datetime.strptime((str(product.created_at)[:10] + ' ' + str(product.created_at)[11:19]),'%Y-%m-%d %H:%M:%S')
                if date > date1:
                    product_numbers += 1
            # for product_variation in ProductAttributes.objects.all():
            #     date = datetime.datetime.strptime((str(product_variation.created_at)[:10] + ' ' + str(product_variation.created_at)[11:19]), '%Y-%m-%d %H:%M:%S')
            #     if date > date1:
            #         product_numbers +=1

            return Response({'number': product_numbers})
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)


class StatisticsOrderNumberView(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)
    serializer_class = StatisticsSerializer

    def post(self, request):
        try:
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
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)


class StatisticsOrderMoneyView(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)
    serializer_class = StatisticsSerializer

    def post(self, request):
        try:
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
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)


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
    queryset = Slider.objects.all().order_by('-id')[:5]


class SliderUpdateView(generics.GenericAPIView, UpdateModelMixin):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)
    serializer_class = SliderSerializer
    queryset = Slider.objects.all()

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

