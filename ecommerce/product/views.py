from rest_framework import generics, permissions, authentication, status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import UpdateModelMixin

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


class SizeCreateView(generics.CreateAPIView):
    serializer_class = SizeSerializer
    queryset = Size.objects.all()


class ProductCreateView(generics.GenericAPIView):
    serializer_class = ProductSerializer
    authentication_classes = (authentication.TokenAuthentication, )
    permission_classes = (permissions.IsAdminUser, )

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        length = request.data.get('length')
        product = request.data.get('product')
        if serializer.is_valid():
            product = serializer.save()

            for file_num in range(0, int(length)):
                images = request.FILES.get(f'images{file_num}')
                ProductImage.objects.create(
                    product=product,
                    images=images
                )
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class ProductListView(generics.ListAPIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)
    serializer_class = ProductSerializer
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