from django.db import models
from django.utils import timezone

from product.models import Product
from main.models import User


class CartProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    is_selected = models.BooleanField(default=False)

    def __str__(self):
        return self.product.category.name


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email


class OrderProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.PositiveIntegerField()

    def __str__(self):
        return self.product.category.name


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_product = models.ManyToManyField(OrderProduct)
    overall_price = models.PositiveIntegerField()
    start_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.user.email


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
