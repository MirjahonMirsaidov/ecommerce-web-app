# Generated by Django 3.1.2 on 2021-03-13 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0014_phoneverify'),
    ]

    operations = [
        migrations.AddField(
            model_name='phoneverify',
            name='verify_kod',
            field=models.PositiveIntegerField(default=543215),
            preserve_default=False,
        ),
    ]
