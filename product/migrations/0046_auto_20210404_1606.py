# Generated by Django 3.1.2 on 2021-04-04 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0045_merge_20210326_1123'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='is_slider',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]