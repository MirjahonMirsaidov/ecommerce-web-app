from django.db import models
from django.utils.text import slugify
from main.models import User


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
    slug = models.SlugField(
        default='',
        editable=False,
    )

    def save(self, *args, **kwargs):
        value = self.name
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    is_import = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.brand} {self.category.name}"


class ProductVariation(models.Model):
    parent = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variations')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='variations')
    name = models.CharField(max_length=255, null=True, blank=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='variations')
    color = models.ForeignKey(Color, on_delete=models.CASCADE, related_name='colors')
    description = models.TextField(null=True, blank=True)
    is_import = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    variation_image = models.ImageField()
    size = models.CharField(max_length=255)
    price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)
    product_code = models.CharField(max_length=7)

    def __str__(self):
        return f"{self.parent.brand.name} {self.category.name} "


class ProductImage(models.Model):
    product = models.ForeignKey(ProductVariation, on_delete=models.CASCADE, related_name='images')
    images = models.ImageField()

    def __str__(self):
        return f"{self.product.parent.brand.name} {self.product.parent.category.name}"


class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    message = models.TextField()
    point = models.CharField(max_length=5)
    created_time = models.DateTimeField(auto_now_add=True)


class Slider(models.Model):
    image = models.ImageField()
    text = models.CharField(max_length=255)
    is_slider = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


