# Generated by Django 4.2.6 on 2024-03-13 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0012_remove_product_product_сollection_product_сollection_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='product_category',
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('CONSTRUCTOR', 'Конструктор'), ('ACCESSORIES', 'Аксессуары'), ('BOOKS', 'Книги')], default=None, help_text='Выберите Категорию', max_length=25, verbose_name='Категория'),
        ),
        migrations.AlterField(
            model_name='product',
            name='сollection',
            field=models.CharField(choices=[('AVATAR', 'Avatar'), ('DC', 'Dc')], help_text='Выберите Коллекцию', max_length=25, verbose_name='Коллекция'),
        ),
    ]
