# Generated by Django 3.1.2 on 2021-05-08 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0049_remove_slider_is_slider'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]