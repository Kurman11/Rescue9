# Generated by Django 3.2.18 on 2023-05-11 02:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_alter_product_is_new'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='is_new',
            field=models.BooleanField(default=False),
        ),
    ]