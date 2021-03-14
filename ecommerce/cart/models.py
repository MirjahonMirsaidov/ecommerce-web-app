from django.db import models
from django.utils import timezone

from product.models import Product
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


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    overall_price = models.PositiveIntegerField()
    is_paid = models.BooleanField(default=False)
    start_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.user.email


class OrderBeta(models.Model):
    name = models.CharField(max_length=25)
    phone_number = models.CharField(max_length=15)
    finish_price = models.PositiveIntegerField()



class OrderProductBeta(models.Model):
    order = models.ForeignKey(OrderBeta, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.PositiveIntegerField()
    price = models.PositiveIntegerField()
    single_overall_price = models.PositiveIntegerField()

    def __str__(self):
        return self.product



class History(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    status = models.CharField(max_length=2, choices=(
        ('P', 'is_paid'),
        ('SH', 'is_shipped'),
        ('F', 'is_finished')
    ))

    def __str__(self):
        return self.product.category.name



class WishList(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishes')

    def __str__(self):
        return self.product.category.name

