# Generated by Django 3.2.18 on 2023-05-11 00:35

from django.db import migrations
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_user_nickname'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='image',
            field=imagekit.models.fields.ProcessedImageField(blank=True, upload_to='users'),
        ),
    ]