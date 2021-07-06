from rest_framework import serializers

from .models import *
from product.serializers import ProductSerializer, ProductGetSerializer


class CartProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer(required=False)

    class Meta:
        model = CartProduct
        fields = ('product', 'count', 'is_selected')


class CartSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cart
        fields = '__all__'


class OrderProductBetaListSerializer(serializers.ModelSerializer):
    product = ProductGetSerializer(required=False)

    class Meta:
        model = OrderProductBeta
        fields = '__all__'


class OrderBetaSerializer(serializers.ModelSerializer):
    orderproducts = OrderProductBetaListSerializer(many=True, required=False)
    class Meta:
        model = OrderBeta
        fields = ('id', 'name', 'phone_number', 'status', 'finish_price', 'orderproducts', )


class OrderProductBetaSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderProductBeta
        fields = ('id',)


class HistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = History
        fields = '__all__'


class WishListSerializer(serializers.ModelSerializer):

    class Meta:
        model = WishList
        fields = '__all__'


class BuySerializer(serializers.Serializer):
    url = serializers.CharField(max_length=50)