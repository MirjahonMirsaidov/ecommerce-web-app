from django.db import models
from django.utils.text import slugify
from main.models import User


class Brand(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Category(models.Model):
    parent = models.IntegerField()
    name = models.CharField(max_length=255)
    image = models.ImageField()
    slug = models.SlugField(
        editable=False,
    )

    def save(self, *args, **kwargs):
        value = self.name
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    parent = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE,)
    category = models.ManyToManyField(Category)
    cover_image = models.ImageField()
    price = models.PositiveIntegerField()
    is_import = models.BooleanField(default=False)
    product_code = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)
<<<<<<< HEAD
    product_code = models.CharField(max_length=7)
=======
    created_at = models.DateTimeField(auto_now_add=True)
>>>>>>> cf4cc2e07195874efc7d0166a91ef08c999d6ab0

    def __str__(self):
        return f"{self.parent.brand.name} {self.category.name} "


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


