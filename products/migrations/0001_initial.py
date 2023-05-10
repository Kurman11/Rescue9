# Generated by Django 3.2.18 on 2023-05-10 04:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import imagekit.models.fields
import products.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('category', models.CharField(max_length=20)),
                ('hits', models.PositiveIntegerField(default=0)),
                ('photo', models.ImageField(upload_to=products.models.product_img_path)),
                ('is_new', models.BooleanField(default=False)),
                ('content', models.TextField()),
                ('like_users', models.ManyToManyField(null=True, related_name='like_product', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('crated_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('content', models.CharField(max_length=600)),
                ('rating', models.FloatField()),
                ('like_users', models.ManyToManyField(null=True, related_name='like_review', to=settings.AUTH_USER_MODEL)),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Review_image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', imagekit.models.fields.ProcessedImageField(blank=True, null=True, upload_to='review/')),
                ('review_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.review')),
            ],
        ),
    ]