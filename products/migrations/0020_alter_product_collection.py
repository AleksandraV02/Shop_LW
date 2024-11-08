# Generated by Django 4.2.6 on 2024-05-13 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0019_rename_сollection_product_collection'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='collection',
            field=models.CharField(choices=[('AVATAR', 'Avatar'), ('DC', 'DC'), ('MARVEL', 'Marvel'), ('INDIANA JONES', 'Indiana Jones'), ('ICONS', 'Icons'), ('JURASSIC WORLD', 'Jurassic World'), ('FRIENDS', 'Friends')], help_text='Выберите Коллекцию', max_length=25, verbose_name='Коллекция'),
        ),
    ]
