from rest_framework import serializers

from .models import *


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class ColorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Color
        fields = '__all__'


class BrandSerializer(serializers.ModelSerializer):

    class Meta:
        model = Brand
        fields = '__all__'


class SizeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Size
        fields = '__all__'


class ProductImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImage
        fields = ('images', )


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, required=False)
    category = CategorySerializer(many=False, required=False)
    colors = ColorSerializer(many=True, required=False)
    class Meta:
        model = Product
        fields = ('id', 'category', 'category_id', 'brand', 'name', 'colors', 'size', 'price', 'quantity', 'images')


