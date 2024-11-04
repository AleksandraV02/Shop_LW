# Generated by Django 4.2.6 on 2024-03-27 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0015_wishlist_delete_favorite'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='age',
            field=models.IntegerField(default=0, max_length=2, verbose_name='Возрастное ограничение'),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5, verbose_name='Цена товара'),
        ),
        migrations.AlterField(
            model_name='product',
            name='total_price',
            field=models.DecimalField(decimal_places=2, default=0, help_text='Цена с учетом скидки', max_digits=5, verbose_name='Скидочная цена'),
        ),
    ]