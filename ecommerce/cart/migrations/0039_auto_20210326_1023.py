# Generated by Django 3.1.2 on 2021-03-26 05:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0043_auto_20210326_0935'),
        ('cart', '0038_auto_20210324_1439'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderproductbeta',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product'),
        ),
    ]