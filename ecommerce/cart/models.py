from django.db import models
from django.utils import timezone

from product.models import Product, ProductAttributes
from main.models import User


class CartProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=1)
    is_selected = models.BooleanField(default=False)

    def __str__(self):
        return self.product.category.name


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email


class OrderBeta(models.Model):

    name = models.CharField(max_length=25)
    phone_number = models.CharField(max_length=255)
    finish_price = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=255, default='Tushgan', choices=(
        ("Tushgan", "Tushgan"),
        ("Kutilmoqda", "Kutilmoqda"),
        ("Bekor qilingan", "Bekor qilingan"),
        ("Tugallangan", "Tugallangan"), ))

    def __str__(self):
        return self.name


class OrderProductBeta(models.Model):
    order = models.ForeignKey(OrderBeta, on_delete=models.CASCADE, related_name='orderproducts')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_code = models.CharField(max_length=7)
    count = models.PositiveIntegerField()
    price = models.PositiveIntegerField()
    single_overall_price = models.PositiveIntegerField()

    def __str__(self):
        return self.product.name


class History(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    

    def __str__(self):
        return self.product.category.name


class WishList(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishes')

    def __str__(self):
        return self.product.category.name


