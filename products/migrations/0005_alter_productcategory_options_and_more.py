# Generated by Django 4.2.6 on 2024-02-25 21:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_alter_product_options_alter_productcategory_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='productcategory',
            options={'ordering': ['id'], 'verbose_name': 'Категория товара', 'verbose_name_plural': 'Категории'},
        ),
        migrations.AlterModelOptions(
            name='producteducations',
            options={'ordering': ['id'], 'verbose_name': "Группа товаров 'Educations'", 'verbose_name_plural': "Группы товаров 'Educations'"},
        ),
        migrations.AlterField(
            model_name='product',
            name='model_number',
            field=models.CharField(default=0, max_length=20, verbose_name='Артикул товара'),
        ),
    ]