# Generated by Django 4.2.6 on 2024-02-14 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_alter_productcategory_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Начальная цена товара'),
        ),
        migrations.AlterField(
            model_name='product',
            name='total_price',
            field=models.DecimalField(decimal_places=2, default=0, help_text='Цена с учетом скидки', max_digits=10, verbose_name='Итоговая цена товара'),
        ),
    ]
