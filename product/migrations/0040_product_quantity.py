# Generated by Django 3.1.2 on 2021-03-25 05:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0039_product_product_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='quantity',
            field=models.PositiveIntegerField(default=4),
            preserve_default=False,
        ),
    ]