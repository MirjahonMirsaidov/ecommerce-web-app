from rest_framework import serializers

from .models import *
from user.serializers import UserSerializer


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



class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, required=False)
    class Meta:
        model = Comment
        fields = ( 'user', 'message', 'point', 'user_id',)



class ProductSerializer(serializers.ModelSerializer):
    brand = BrandSerializer(many=False, required=False)
    category = CategorySerializer(many=False, required=False)
    
    class Meta:
        model = Product
        fields = ('id', 'category', 'brand', 'name', 'description', 'cover_image', )


class ProductDetailSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, required=False)
    brand = BrandSerializer(many=False, required=False)
    category = CategorySerializer(many=False, required=False)
    
    comments = CommentSerializer(many=True, required=False)
    class Meta:
        model = Product
        fields = ('id', 'category', 'brand', 'name', 'cover_image', 'comments')



