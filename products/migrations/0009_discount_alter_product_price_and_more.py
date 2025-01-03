# Generated by Django 4.2.6 on 2024-03-07 07:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_rename_total_price_productdiscount_discount_price_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price_no_discount', models.DecimalField(decimal_places=2, default=0, max_digits=5, verbose_name='Начальная цена')),
                ('discount_active', models.BooleanField(default=False, verbose_name='Активность скидки')),
                ('discount', models.IntegerField(default=0, help_text='Укажите % скидки', verbose_name='Скидка %')),
                ('discount_price', models.DecimalField(decimal_places=2, default=0, max_digits=5, verbose_name='Итоговая цена товара')),
            ],
            options={
                'verbose_name': 'Товар со скидкой',
                'verbose_name_plural': 'Товары со скидкой',
                'ordering': ['discount'],
            },
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5, verbose_name='Начальная цена товара'),
        ),
        migrations.AlterField(
            model_name='product',
            name='total_price',
            field=models.DecimalField(decimal_places=2, default=0, help_text='Цена с учетом скидки', max_digits=5, verbose_name='Итоговая цена'),
        ),
        migrations.DeleteModel(
            name='ProductDiscount',
        ),
        migrations.AddField(
            model_name='discount',
            name='product',
            field=models.ForeignKey(blank=True, default=None, help_text='Выберите товар', null=True, on_delete=django.db.models.deletion.CASCADE, to='products.product', verbose_name='Товар'),
        ),
    ]
