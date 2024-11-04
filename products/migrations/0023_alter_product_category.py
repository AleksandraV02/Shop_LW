# Generated by Django 4.2.6 on 2024-08-17 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0022_alter_product_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('CONSTRUCTOR', 'Конструктор'), ('ACCESSORIES', 'Аксессуары'), ('BOOKS', 'Книги и журналы')], default=None, help_text='Выберите Категорию', max_length=25, verbose_name='Категория'),
        ),
    ]
