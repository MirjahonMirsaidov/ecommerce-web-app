from rest_framework import serializers

from .models import *
from user.serializers import UserSerializer


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', )


class ColorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Color
        fields = '__all__'


class BrandSerializer(serializers.ModelSerializer):

    class Meta:
        model = Brand
        fields = ('name',)


class ProductImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImage
        fields = ('images', )


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, required=False)
    class Meta:
        model = Comment
        fields = ( 'user', 'message', 'point', 'user_id',)


class ProductVariationSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, required=False)

    class Meta:
        model = ProductVariation
        fields = ('parent_id', 'size', 'color', 'price', 'variation_image', 'quantity', 'images')


class ProductVariationGetSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, required=False)
    color = ColorSerializer(many=False, required=False)

    class Meta:
        model = ProductVariation
        fields = ('id', 'parent_id', 'name', 'description', 'is_import', 'created_at', 'size', 'color', 'price', 'variation_image', 'quantity', 'images')


class ProductGetSerializer(serializers.ModelSerializer):
    brand = BrandSerializer(many=False, required=False)
    category = CategorySerializer(many=False, required=False)
    variations = ProductVariationGetSerializer(many=True, required=False)

    class Meta:
        model = Product
        fields = ('id', 'category', 'brand', 'name', 'description', 'cover_image', 'variations',)


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'


class ProductDetailSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, required=False)
    brand = BrandSerializer(many=False, required=False)
    category = CategorySerializer(many=False, required=False)
    comments = CommentSerializer(many=True, required=False)

    class Meta:
        model = Product
        fields = ('id', 'category', 'brand', 'name', 'cover_image', 'images', 'comments')



