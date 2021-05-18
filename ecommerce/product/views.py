import datetime
import os
from django.db.models import Q, Max
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
    def post(self, request):
        try:
            name = request.data.get('name').lower()
            parent_id = request.data.get('parent_id')
            image = request.data.get('image')
            order = request.data.get('order')
            is_slider = str(request.data.get('is_slider')).capitalize()
            if parent_id == 'null':
                parent_id = 0
            if order == 'null':
                order = 0
            if name and image:
                if not Category.objects.filter(name=name, parent_id=parent_id, order=order, is_slider=is_slider):
                    Category.objects.get_or_create(name=name, parent_id=parent_id, image=image, order=order, is_slider=is_slider)
                    return Response("Kategoriya muvaffaqiyatli qo'shildi", status=status.HTTP_201_CREATED)
                return Response("Mavjud kategoriyani qo'shdingiz!", status=status.HTTP_400_BAD_REQUEST)
            return Response("Ma'lumotlar xato kiritilgan", status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response("Ma'lumotlar xato kiritilgan", status=status.HTTP_400_BAD_REQUEST)


class CategoryAllListView(generics.ListAPIView):
    serializer_class = CategorySerializer
    pagination_class = CustomPagination
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    filter_fields = ['parent_id']
    CustomPagination.page_size = 10
    def get_queryset(self):
        try:
            return Category.objects.all()
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)


class CategoryListView(generics.GenericAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    def get(self, request):
        try:
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
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

class CategoryChildListView(APIView):

    def get(self, request, id):
        try:
            categories = Category.objects.filter(parent_id=id)
            categories = CategorySerializer(categories, many=True)
            return Response(categories.data)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)


class CategoryDeleteView(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)

    def delete(self, request, id):
        try:
            if (not Category.objects.get(id=id).is_slider == True) or Category.objects.filter(is_slider=True).count() > 3:
                if not CategoryProduct.objects.filter(category_id=id):
                    for category in Category.objects.filter(Q(id=id) | Q(parent_id=id)):
                        category.delete()
                    return Response("Kategoriya muvaffaqiyatli o'chirildi", status=status.HTTP_200_OK)
                return Response("Maxsulotlar bilan bog'lanish mavjud kategoriyani o'chirish mumkin emas", status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response("Slayder uchun kamida 3 ta kategoriya qolishi kerak", status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)


class CategoryDetailView(generics.RetrieveAPIView):
    serializer_class = CategorySerializer
    def get_queryset(self):
        try:
            return Category.objects.all()
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

class CategoryUpdateView(generics.GenericAPIView, UpdateModelMixin):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)
    serializer_class = CategorySerializer
    queryset = CategorySerializer

    def patch(self, request, pk):
        try:
            category = Category.objects.get(id=pk)
            sliders = Category.objects.filter(is_slider=True).count()
            is_slider = str(request.data.get('is_slider')).capitalize()
            if sliders == 3 and is_slider=='False' and category.is_slider == True:
                is_slider = True
                msg = "Slayderga eng kamida 3 ta kategoriya chiqishi kerak"
            else:
                msg = "Muvaffaqiyatli o'zgartirildi"
            order = request.data.get('order')
            parent_id = request.data.get('parent_id')
            image = request.data.get('image')
            name = request.data.get('name')
            if order == 'null':
                order = 0
            if parent_id == 'null':
                parent_id = 0
            if image == 'null' or not image:
                image = category.image
            category.image = image
            category.is_slider = is_slider
            category.name = name
            category.order = order
            category.parent_id = parent_id
            category.save()
            return Response(msg, status=status.HTTP_200_OK)
        except:
            return Response("Ma'lumotlar xato kiritilgan", status=status.HTTP_400_BAD_REQUEST)


class CategorySliderView(generics.ListAPIView):
    serializer_class = CategorySerializer
    pagination_class = CustomPagination
    CustomPagination.page_size = 10
    def get_queryset(self):
        try:
            return Category.objects.filter(is_slider=True).order_by('-updated_at')[:3]
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

class BrandCreateView(generics.CreateAPIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)
    serializer_class = BrandSerializer
    def post(self, request):
        try:
            serializer = BrandSerializer(data=request.data)
            brand = request.data.get('name').lower()
            if serializer.is_valid():
                brands = Brand.objects.all()
                for bd in brands:
                    if bd.name.lower() == brand:
                        return Response("Mavjud brend qo'shildi", status=status.HTTP_400_BAD_REQUEST)
                Brand.objects.create(name=brand)
                return Response("Brend muvaffaqiyatli qo'shildi", status=status.HTTP_201_CREATED)
            return Response("Ma'lumotlar xato kiritilgan", status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response("Ma'lumotlar xato kiritilgan", status=status.HTTP_400_BAD_REQUEST)

class BrandListView(generics.ListAPIView):
    serializer_class = BrandSerializer
    pagination_class = CustomPagination
    CustomPagination.page_size = 10
    def get_queryset(self):
        try:
            return Brand.objects.all()
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

class BrandDeleteView(generics.DestroyAPIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)
    serializer_class = BrandSerializer
    queryset = Brand.objects.all()

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            if instance:
                self.perform_destroy(instance)
                return Response("Brend muvaffaqiyatli o'chirildi", status=status.HTTP_200_OK)
            return Response("So'rovda xatolik mavjud", status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)


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
            is_import = str(request.data.get('is_import')).capitalize()
            price = request.data.get('price')
            parent_id = request.data.get('parent_id')
            quantity = request.data.get('quantity')
            prod_image = request.data.get('image')
            product_code = request.data.get('product_code')
            categories = request.data.get('categories')
            attributes = request.data.get('attributes')
            images = request.data.get('images')
            variations = request.data.get('variations')
            if serializer.is_valid():
                if len(images) < 6:
                    if not check_product_exists(product_code, attributes):
                        if get_image_from_data_url(prod_image):
                            if variations:
                                product = Product.objects.create(
                                    name=name,
                                    description=description,
                                    brand_id=brand,
                                    is_import=is_import,
                                    price=price,
                                    parent_id=parent_id,
                                    quantity=quantity,
                                    image=get_image_from_data_url(prod_image)[0],
                                    product_code=product_code,
                                )
                                if categories:
                                    save_category(categories, product)

                                if attributes:
                                    save_attribute(attributes, product)

                                if images:
                                    save_image(images, product)

                                for variation in variations:
                                    print(variation['name'])
                                    if variation['image']:
                                        image = variation['image']
                                    else:
                                        image = product.image
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
                                            var_product.save()
                                            print(var_product.name)


                                            var_categories = variation['categories']
                                            if var_categories:
                                                save_category(var_categories, var_product)
                                            else:
                                                save_category(categories, var_product)

                                            var_attributes = variation['attributes']
                                            if var_attributes:
                                                save_attribute(var_attributes, var_product)
                                            else:
                                                save_attributes(attributes, var_product)

                                            imagesa = variation['images']
                                            if imagesa:
                                                save_image(imagesa, var_product)
                                            else:
                                                save_image(images, var_product)

                                        else:
                                            return Response("png, jpg, jpeg, webp, Rasm kiriting", status=status.HTTP_400_BAD_REQUEST)
                                    else:
                                        return Response("Bir xil variatsiyali maxsulot qo'shdingiz!", status=status.HTTP_208_ALREADY_REPORTED)
                                return Response(serializer.data, status=status.HTTP_200_OK)
                            else:
                                product = Product.objects.create(
                                    name=name,
                                    description=description,
                                    brand_id=brand,
                                    is_import=is_import,
                                    price=price,
                                    parent_id=parent_id,
                                    quantity=quantity,
                                    image=get_image_from_data_url(prod_image)[0],
                                    product_code=product_code,
                                )
                                if categories:
                                    save_category(categories, product)

                                if attributes:
                                    save_attribute(attributes, product)

                                if images:
                                    save_image(images, product)
                                return Response(serializer.data, status=status.HTTP_200_OK)
                        return Response("png, jpg, jpeg, webp, Rasm kiriting", status=status.HTTP_400_BAD_REQUEST)
                    else:
                        return Response("Bu maxsulot allaqachon qo'shilgan!", status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response("Rasmlar soni 5 dan ko'p bolishi mumkin emas", status=status.HTTP_400_BAD_REQUEST)
            return Response("Ma'lumotlar to'liq emas", status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response("Ma'lumotlar xato kiritilgan", status=status.HTTP_400_BAD_REQUEST)


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
                    return Response("Muvaffaqiyatli qo'shildi", status=status.HTTP_200_OK)
                else:
                    return Response("Bu maxsulot variatsiya oldin qo'shilgan", status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response("Rasmlar soni 8tadan ko'p bolishi mumkin emas", status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response("Ma'lumotlar xato kiritilgan", status=status.HTTP_400_BAD_REQUEST)


class ProductListView(generics.ListAPIView):
    serializer_class = ProductGetSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'product_code', ]
    filter_fields = ['brand', 'parent_id', 'is_import']
    ordering_fields = ['created_at', 'price']
    pagination_class = CustomPagination
    CustomPagination.page_size = 10

    def get_queryset(self):
        try:
            min = self.request.GET.get('min')
            max = self.request.GET.get('max')
            if not min or min == '':
                min = 0
            if not max or max == '':
                max = Product.objects.all().order_by('-price').first().price
            categories = self.request.query_params.getlist('category[]')
            if categories and not categories[0] == '':
                products = Product.objects.filter(id=-1)
                for category in categories:
                    category_products = CategoryProduct.objects.filter(category_id=category)
                    for prod in category_products:
                        id = prod.product_id
                        product = Product.objects.get(id=id)
                        products |= Product.objects.filter(id=product.id)

                if min or max:
                    products = products.filter(status=True, price__range=(min, max)).select_related('brand').order_by('-id')
            elif min or max:
                products = Product.objects.filter(status=True, price__range=(min, max)).select_related('brand').order_by('-id')
            else:
                products = Product.objects.filter(status=True).select_related('brand', ).order_by('-id')

            return products
        except:
            return Product.objects.filter(id=-1)


class CodeSizeListView(APIView):

    def get(self, request):
        try:
            li = []
            for product in Product.objects.all():
                if ProductAttributes.objects.filter(product=product).exists():
                    for attr in ProductAttributes.objects.filter(product=product):
                        if attr.key == 'size':
                            li.append({
                                "id": product.id,
                                "codesize": f'kod: {product.product_code}    o`lcham: {attr.value}',
                                "product_code": product.product_code,
                                "size": attr.value,

                            })
            return Response(li)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)


class ProductsByCategoryView(generics.ListAPIView):
    serializer_class = ProductGetSerializer
    queryset = Product.objects.all()
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filter_fields = ['brand', 'parent_id', 'is_import', ]
    search_fields = ['name', 'product_code']
    ordering_fields = ['created_at', 'price']
    pagination_class = CustomPagination
    CustomPagination.page_size = 10

    def get_queryset(self):
        try:
            slug = self.kwargs['slug']
            min = self.request.GET.get('min')
            max = self.request.GET.get('max')

            if Category.objects.filter(slug=slug).exists():
                print("Bor 443")
                category = Category.objects.get(slug=slug)
                products = []
                if min =='':
                    min=0
                if max == '':
                    max = Product.objects.all().aggregate(Max('price'))

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

                if min or max:
                    return Product.objects.filter(id__in=products, price__range=(min, max)).select_related('brand')
                else:
                    return Product.objects.filter(id__in=products).select_related('brand')
            else:
                return Product.objects.filter(id=-1)

        except:
            return Product.objects.filter(id=-1)



class ProductUpdateView(GenericAPIView, UpdateModelMixin):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)
    queryset = Product.objects.all()
    serializer_class = ProductUpdateSerializer

    def patch(self, request, pk):
        try:
            serializer = ProductUpdateSerializer(data=request.data)
            product = Product.objects.get(id=pk)
            product.name = request.data.get('name')
            product.description = request.data.get('description')
            product.product_code = request.data.get('product_code')
            product.price = request.data.get('price')
            product.quantity = request.data.get('quantity')
            image = request.data.get('image')
            brand = product.brand
            if image == 'null' or image=='undefined':
                image = product.image
            if serializer.is_valid():
                product.image = image
                product.save()
                return Response("Maxsulot muvaffaqiyatli o'zgartirildi.", status=status.HTTP_200_OK)
            return Response("Ma'lumotlar to'liq emas", status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response("Ma'lumotlar xato kiritilgan", status=status.HTTP_400_BAD_REQUEST)


class ProductDeleteView(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)

    def delete(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
            if product.parent_id == 0:
                product.status=False
                product.save()
                return Response("")
            else:
                product.delete()
                for item in CategoryProduct.objects.filter(product_id=pk):
                    item.delete()
                return Response("Maxsulot o'chirildi", status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)


class ProductDetailView(generics.GenericAPIView):
    serializer_class = ProductGetSerializer
    queryset = Product.objects.all()

    def get(self, request, id):
        try:
            variations_list = []
            product = Product.objects.get(id=id)
            child = product
            if product.parent_id:
                parent = Product.objects.get(id=product.parent_id)
                product_variations = Product.objects.filter(parent_id=parent.id).select_related('brand')
            else:
                parent = Product.objects.get(id=product.id)
                product_variations = Product.objects.filter(parent_id=id).select_related('brand')

            if parent.status==True:
                variations_list.append({
                    "id": parent.id,
                    "parent_id": parent.parent_id,
                    "name": parent.name,
                    "description": parent.description,
                    "product_code": parent.product_code,
                    "is_import": parent.is_import,
                    "brand": {
                        "id": parent.brand_id,
                        "name": parent.brand.name,
                    },
                    "categories": get_categories(parent),
                    "attributes": get_attributes(parent.id),
                    "price": parent.price,
                    "image": "http://127.0.0.1:8000" + parent.image.url,
                    "quantity": parent.quantity,
                    "images": get_images(parent),
                    "created_at": parent.created_at,
                })

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
            return Response(
                variations_list
            )
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)


class ProductSpecificDetailView(generics.GenericAPIView):
    serializer_class = ProductGetSerializer
    queryset = Product.objects.all()

    def get(self, request, id):
        try:
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
                "description": product.description,
                "price": product.price,
                "quantity": product.quantity,
                "image": "http://127.0.0.1:8000" + product.image.url,
                "images": get_images(product),
            })
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

class ProductAttributesListView(generics.ListAPIView):
    serializer_class = ProductAttributesSerializer
    def get_queryset(self):
        try:
            return ProductAttributes.objects.all()
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

class ProductAttributesDeleteView(generics.DestroyAPIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)
    serializer_class = ProductAttributesSerializer
    queryset = ProductAttributes.objects.all()

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            if instance:
                self.perform_destroy(instance)
                return Response("Attribut muvaffaqiyatli o'chirildi", status=status.HTTP_200_OK)
            return Response("So'rovda xatolik mavjud", status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)


class ProductAttributesUpdateView(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)

    def post(self, request):
        try:
            attributes = request.data.get('attributes')
            product = int(request.data.get('product'))
            if len(attributes)>1:
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

                return Response("Maxsulot attributlari muvaffaqiyatli yangilandi", status=status.HTTP_200_OK)
            return Response("Kamida 2 ta attribut (Rang va o'lcham) bo'lishi kerak", status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response("Ma'lumotlar xato kiritilgan", status=status.HTTP_400_BAD_REQUEST)


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
                    image = ProductImage.objects.filter(product_id=product, images=img)
                    image.delete()
                    try:
                        os.remove(img)
                        print("% s removed successfully" % img)
                    except:
                        print("File path can not be removed")
            if images:
                for image in images:
                        ProductImage.objects.create(
                            product_id=product,
                            images=get_image_from_data_url(image)[0],
                        )
            return Response("Maxsulot rasmlari muvaffaqiyatli o'zgartirildi", status=status.HTTP_200_OK)
        except:
            return Response("Ma'lumotlar xato kiritilgan", status=status.HTTP_400_BAD_REQUEST)


class ProductCategoryUpdateView(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)

    def post(self, request):
        try:
            product = request.data.get('product')
            categories_list = request.data.get('categories')
            if categories_list:
                if all(isinstance(category, int) for category in categories_list):
                    category_products = CategoryProduct.objects.filter(product_id=product)
                    for item in category_products:
                        if item.category_id not in categories_list:
                            item.delete()
                    for category in categories_list:
                        CategoryProduct.objects.get_or_create(category_id=category,
                                                                product_id=product)
                    return Response("Maxsulot kategoriyalari muvaffaqiyatli yangilandi", status=status.HTTP_200_OK)
                return Response("Kategoriyalar ro'yxati noto'g'ri kiritilgan", status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response("Mahsulotda kamida 1ta kategoriya bo'lishi kerak", status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response("Ma'lumotlar xato kiritilgan",status=status.HTTP_400_BAD_REQUEST)


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
    def post(self, request):
        try:
            serializer = SliderSerializer(data=request.data)
            image = request.data.get('image')
            text = request.data.get('text')
            category = request.data.get('category')
            if serializer.is_valid():
                check = Slider.objects.filter(text=text, category=category).exists()
                if not check:
                    serializer.save()
                    return Response("Slayder muvaffaqiyatli qo'shildi", status=status.HTTP_201_CREATED)
                return Response("Slayder oldin qo'shilgan", status=status.HTTP_400_BAD_REQUEST)
            return Response("Kiritilgan ma'lumotlar to'liq emas", status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response("Ma'lumotlar xato kiritilgan", status=status.HTTP_400_BAD_REQUEST)


class SliderDeleteView(generics.DestroyAPIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)
    serializer_class = SliderSerializer
    queryset = Slider.objects.all()

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            if instance:
                self.perform_destroy(instance)
                return Response("Slayder muvaffaqiyatli o'chirildi", status=status.HTTP_200_OK)
            return Response("So'rovda xatolik mavjud", status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)


class SliderDetailView(generics.RetrieveAPIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)
    serializer_class = SliderGetSerializer
    def get_queryset(self):
        try:
            return Slider.objects.all()
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)


class SliderListView(generics.ListAPIView):
    serializer_class = SliderGetSerializer
    def get_queryset(self):
        try:
            return Slider.objects.all().order_by('-id')[:5]
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)


class SliderAllListView(generics.ListAPIView):
    serializer_class = SliderGetSerializer
    pagination_class = CustomPagination
    CustomPagination.page_size = 10
    def get_queryset(self):
        try:
            return Slider.objects.all()
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)


class SliderUpdateView(generics.GenericAPIView, UpdateModelMixin):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)
    serializer_class = SliderSerializer
    queryset = Slider.objects.all()

    def patch(self, request, *args, **kwargs):
        try:
            self.partial_update(request, *args, **kwargs)
            return Response("Slayder muvaffaqiyatli o'zgartirildi", status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)


class AddCommentView(generics.GenericAPIView):
    serializer_class = CommentSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        try:
            serializer = CommentSerializer(data=request.data)
            user = request.user
            product_id = request.data.get('product_id')
            message = request.data.get('message')
            point = request.data.get('point')
            if serializer.is_valid():
                comment_check = Comment.objects.filter(product_id=product_id, user_id=user.pk)
                if comment_check.exists():
                    return Response('Yes')
                else:
                    Comment.objects.create(product_id=product_id, user_id=user.pk, message=message, point=point)
                return Response('Okay')
            return Response('Serializer not valid')
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)


class UpdateCommentView(generics.GenericAPIView):
    serializer_class = CommentSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def patch(self, request, pk):
        try:
            comment = Comment.objects.get(id=pk)
            serializer = CommentSerializer(comment, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)


class DeleteCommentView(generics.GenericAPIView):
    serializer_class = CommentSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def delete(self, request, id):
        try:
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
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
