from rest_framework import serializers

from .models import *
from user.serializers import UserSerializer


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class BrandSerializer(serializers.ModelSerializer):

    class Meta:
        model = Brand
        fields = '__all__'


class ProductImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImage
        fields = ('images', )


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('parent_id', 'product_code', 'name', 'description', 'is_import', 'created_at', 'category', 'brand', 'size', 'price', 'cover_image', 'quantity')


class ProductGetSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, required=False)
    brand = BrandSerializer(many=False, required=False)
    category = CategorySerializer(many=True, required=False)

    class Meta:
        model = Product
        fields = ('id', 'parent_id', 'product_code', 'name', 'description', 'is_import', 'created_at', 'category', 'brand', 'size', 'price', 'cover_image', 'quantity', 'images')


class StatisticsSerializer(serializers.Serializer):
    date = serializers.IntegerField()


class SliderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slider
        fields = '__all__'


class SliderGetSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=False, required=False)
    class Meta:
        model = Slider
        fields = ('id', 'image', 'text', 'category')


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, required=False)

    class Meta:
        model = Comment
        fields = ('user', 'message', 'point', 'user_id',)

