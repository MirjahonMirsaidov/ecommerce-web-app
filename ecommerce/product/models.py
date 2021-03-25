from django.db import models
from django.utils.text import slugify
from main.models import User


class Brand(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255)
    parent_id = models.PositiveIntegerField(default=0)
    image = models.ImageField()
    order = models.IntegerField(default=0)
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
    description = models.TextField(null=True, blank=True)
    price = models.PositiveIntegerField()
    parent_id = models.PositiveIntegerField(null=True, blank=True)
    is_import = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    product_code = models.CharField(max_length=7)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.brand} {self.name}"


class CategoryProduct(models.Model):
    category_id = models.PositiveIntegerField()
    product_id = models.PositiveIntegerField()

    def __int__(self):
        return f"{self.category_id}"


class ProductAttributes(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='attributes')
    is_main = models.BooleanField(default=False)
    key = models.CharField(max_length=255)
    label = models.CharField(max_length=255)
    value = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.brand.name}"


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
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


