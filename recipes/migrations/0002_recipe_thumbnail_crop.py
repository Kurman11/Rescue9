# Generated by Django 3.2.18 on 2023-05-15 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='thumbnail_crop',
            field=models.ImageField(default=1, upload_to='thumbnail_crop'),
            preserve_default=False,
        ),
    ]