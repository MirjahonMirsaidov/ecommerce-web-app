from django.db import models


class Color(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Size(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    description = models.CharField(max_length=255, null=True, blank=True)
    price = models.PositiveIntegerField()
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    is_import = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.brand} {self.category}"


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    images = models.ImageField()

    def __str__(self):
        return f"{self.product.brand} {self.product.category}"
