# Generated by Django 3.1.2 on 2021-03-14 10:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0007_auto_20210310_1115'),
        ('cart', '0018_orderbeta'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderbeta',
            old_name='count',
            new_name='finish_price',
        ),
        migrations.RemoveField(
            model_name='orderbeta',
            name='overall_price',
        ),
        migrations.RemoveField(
            model_name='orderbeta',
            name='product',
        ),
        migrations.CreateModel(
            name='OrderProductBeta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.PositiveIntegerField()),
                ('price', models.PositiveIntegerField()),
                ('single_overall_price', models.PositiveIntegerField()),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cart.orderbeta')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product')),
            ],
        ),
    ]