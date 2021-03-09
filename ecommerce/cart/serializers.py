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


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
<<<<<<< HEAD
        fields = '__all__'
=======
        fields = ('cart_product', )
>>>>>>> 922f6f5ed67ea4f481466718c1c877ed72d9ae89


class HistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = History
        fields = '__all__'


class BuySerializer(serializers.Serializer):
    url = serializers.CharField(max_length=50)