# Generated by Django 3.1.2 on 2021-03-24 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0027_productvariation_product_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='image',
            field=models.ImageField(default=123, upload_to=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='category',
            name='order',
            field=models.IntegerField(default=3),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='category',
            name='parent_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]