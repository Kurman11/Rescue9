# Generated by Django 3.2.18 on 2023-05-11 14:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_commentimage_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='commentimage',
            name='name',
        ),
    ]
