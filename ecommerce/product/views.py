from rest_framework import generics, permissions
from rest_framework.response import Response
from django.contrib.auth.decorators import permission_required

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
    permission_classes = (permissions.IsAdminUser, )

    # def post(self, request):


