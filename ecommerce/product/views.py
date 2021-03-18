from django_filters.rest_framework import DjangoFilterBackend
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


class ColorCreateView(generics.CreateAPIView):
    serializer_class = ColorSerializer
    queryset = Color.objects.all()


class BrandCreateView(generics.CreateAPIView):
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
        name = request.data.get('name')
        description = request.data.get('description')
        size = request.data.get('size')
        color = request.data.get('color')
        price = request.data.get('price')
        quantity = request.data.get('quantity')

        if serializer.is_valid():
            product = serializer.save()

            for file_num in range(0, int(length)):
                images = request.FILES.get(f'images{file_num}')
                ProductImage.objects.create(
                    parent=parent,
                    images=images,
                )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
            variations = ProductVariation.objects.filter(category_id=category.id)
            serializer = ProductVariationGetSerializer(variations, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response('Not found')

class ProductListView(generics.ListAPIView):
    # authentication_classes = (authentication.TokenAuthentication,)
    # permission_classes = (permissions.IsAdminUser,)
    serializer_class = ProductGetSerializer
    queryset = Product.objects.all()
    filter_fields = ['category']



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


class ImportedProductsView(generics.ListAPIView):
    serializer_class = ProductGetSerializer
    queryset = Product.objects.filter(is_import=True)


class LocalProductsView(generics.ListAPIView):
    serializer_class = ProductGetSerializer
    queryset = Product.objects.filter(is_import=False)


class ProductByCategoryView(generics.ListAPIView):
    serializer_class = ProductGetSerializer

    def get_queryset(self):
        category_products = Product.objects.all()
        slug = self.kwargs['slug']
        category_id = Category.objects.get(slug=slug).id
        if category_id is not None:
            category_products = Product.objects.filter(category_id=category_id)
        return category_products


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
