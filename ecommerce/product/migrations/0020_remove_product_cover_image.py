# Generated by Django 3.1.2 on 2021-03-19 09:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0019_auto_20210319_0952'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='cover_image',
        ),
    ]