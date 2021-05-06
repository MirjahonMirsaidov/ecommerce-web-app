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


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, required=False)

    class Meta:
        model = Comment
        fields = ('user', 'message', 'point', 'user_id',)


class ProductAttributesSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductAttributes
        fields = '__all__'


class ProductGetSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, required=False)
    brand = BrandSerializer(many=False, required=False)
    attributes = ProductAttributesSerializer(many=True, required=False)
   
    class Meta:
        model = Product
        fields = ('id', 'parent_id', 'product_code', 'name', 'description', 'image', 'is_import', 'created_at', 'brand',
                  'price', 'quantity', 'images', 'attributes')


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'


class ProductUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('name', 'description', 'product_code', 'price', 'quantity')


class ProductVariationSerializer(serializers.ModelSerializer):
    image = serializers.CharField(max_length=100000000000, allow_blank=True)
    attributes = serializers.ListField()
    images = serializers.ListField(str)
    categories = serializers.ListField()

    class Meta:
        model = Product
        fields = ('product_code', 'name', 'description', 'image', 'price', 'quantity', 'images',
                  'attributes', 'categories')


class ProductCreateSerializer(serializers.ModelSerializer):
    variations = ProductVariationSerializer(required=False, many=True)
    image = serializers.CharField(max_length=100000000000)
    attributes = serializers.ListField()
    images = serializers.ListField()
    categories = serializers.ListField()

    class Meta:
        model = Product
        fields = ('parent_id', 'product_code', 'name', 'description', 'image', 'is_import', 'brand',
                  'price', 'quantity', 'images', 'attributes', 'variations', 'categories')


class ProductDetailSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, required=False)
    brand = BrandSerializer(many=False, required=False)

    class Meta:
        model = Product
        fields = ('id', 'brand', 'name', 'images', )


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