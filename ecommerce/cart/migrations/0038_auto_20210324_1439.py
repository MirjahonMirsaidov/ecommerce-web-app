# Generated by Django 3.1.2 on 2021-03-24 09:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0031_auto_20210324_1439'),
        ('cart', '0037_auto_20210323_1723'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderproductbeta',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.productattributes'),
        ),
    ]