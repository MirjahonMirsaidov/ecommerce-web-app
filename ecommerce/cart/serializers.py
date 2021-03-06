from rest_framework import serializers

from .models import *
from product.serializers import ProductSerializer


class CartProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer(required=False)

    class Meta:
        model = CartProduct
        fields = ('product', 'count')


class CartSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cart
        fields = '__all__'


# class OrderProductSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = OrderProduct
#         fields = '__all__'


# class OrderSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Order
#         fields = '__all__'


class HistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = History
        fields = '__all__'