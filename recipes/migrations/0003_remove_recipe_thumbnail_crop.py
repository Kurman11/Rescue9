# Generated by Django 3.2.18 on 2023-05-12 07:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_rename_thumbnail_recipe_thumbnail_crop'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='thumbnail_crop',
        ),
    ]