# Generated by Django 3.1.2 on 2021-03-24 09:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0038_auto_20210324_1439'),
        ('product', '0031_auto_20210324_1439'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ProductVariation',
        ),
        migrations.AddField(
            model_name='productattributes',
            name='brand',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='variations', to='product.brand'),
        ),
        migrations.AddField(
            model_name='productattributes',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='variations', to='product.category'),
        ),
        migrations.AddField(
            model_name='productattributes',
            name='color',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='colors', to='product.color'),
        ),
        migrations.AddField(
            model_name='productattributes',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='variations', to='product.product'),
        ),
    ]
