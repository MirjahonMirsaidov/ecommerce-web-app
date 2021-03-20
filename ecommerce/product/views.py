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


class CategoryCreateView(generics.CreateAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class CategoryListView(generics.ListAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class ColorCreateView(generics.CreateAPIView):
    serializer_class = ColorSerializer
    queryset = Color.objects.all()


class ColorListView(generics.ListAPIView):
    serializer_class = ColorSerializer
    queryset = Color.objects.all()


class BrandCreateView(generics.CreateAPIView):
    serializer_class = BrandSerializer
    queryset = Brand.objects.all()


class BrandListView(generics.ListAPIView):
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
        length = request.data.get('length')
        parent = request.data.get('parent')
        size = request.data.get('size')
        color = request.data.get('color')
        price = request.data.get('price')
        variation_image = request.data.get('variation_image')
        quantity = request.data.get('quantity')
        name = Product.objects.get(id=parent).name
        brand = Product.objects.get(id=parent).brand
        category_id = Product.objects.get(id=parent).category_id
        description = Product.objects.get(id=parent).description
        is_import = Product.objects.get(id=parent).is_import
        if serializer.is_valid():
            product = ProductVariation.objects.create(parent_id=parent, category_id=category_id, name=name, brand=brand, description=description, is_import=is_import, size=size, color_id=color, price=price, variation_image=variation_image, quantity=quantity)

            for file_num in range(0, int(length)):
                images = request.FILES.get(f'images{file_num}')
                ProductImage.objects.create(
                    product=product,
                    images=images,
                )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VariationListView(generics.ListAPIView):
    serializer_class = ProductVariationGetSerializer
    queryset = ProductVariation.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filter_fields = ['is_import', 'category', 'color', 'brand', ]
    search_fields = ['name', ]


class VariationDetailView(generics.RetrieveAPIView):
    serializer_class = ProductVariationGetSerializer
    queryset = ProductVariation.objects.all()


class ProductVariationListView(generics.GenericAPIView):
    serializer_class = ProductVariationGetSerializer
    queryset = ProductVariation.objects.all()

    def get(self, request, id):
        products = ProductVariation.objects.filter(parent_id=id)
        serializer = ProductVariationGetSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductVariationByCategory(generics.GenericAPIView):
    serializer_class = ProductVariationGetSerializer
    queryset = ProductVariation.objects.all()

    def get(self, request, slug):
        category = Category.objects.get(slug=slug)
        if category:
            variation = ProductVariation.objects.filter(category_id=category.id)
            serializer = ProductVariationGetSerializer(variation, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductListView(generics.ListAPIView):
    # authentication_classes = (authentication.TokenAuthentication,)
    # permission_classes = (permissions.IsAdminUser,)
    serializer_class = ProductGetSerializer
    queryset = Product.objects.all()


class ProductDetailView(generics.RetrieveAPIView):
    serializer_class = ProductGetSerializer
    queryset = Product.objects.all()


class ProductUpdateView(GenericAPIView, UpdateModelMixin):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def put(self, request, *args, **kwargs):
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


class ImportedProductsView(generics.ListAPIView):
    serializer_class = ProductGetSerializer
    queryset = Product.objects.filter(is_import=True)


class LocalProductsView(generics.ListAPIView):
    serializer_class = ProductGetSerializer
    queryset = Product.objects.filter(is_import=False)


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
