from django.db import models
from django.conf import settings
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import Thumbnail, ResizeToFit
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.
def comment_img_path(instance, filename):
    return f'images/comment/{instance.name}/{filename}'

def recipe_thumbnail_path(instance, filename):
    return f'images/recipe/thumbnail/{instance.title}/{filename}'

def recipe_thumbnail_path(instance, filename):
    return f'images/recipe/thumbnail/{instance.title}/{filename}'


class Recipe(models.Model):
    title = models.CharField(max_length=20)
    thumbnail_upload = models.ImageField(upload_to=recipe_thumbnail_path)
    thumbnail = ImageSpecField(
        source = 'thumbnail_upload',
        processors = [Thumbnail(100, 100)],
        format='JPEG',
        options={'quality': 60},
        )
    category = models.CharField(max_length=20)
    hits = models.PositiveIntegerField()
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="like_recipes")
    content = RichTextUploadingField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    used_products = models.ManyToManyField("products.Product", related_name="used_recipes")


class Comment(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    content = models.TextField()
    like_user = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="like_comments")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class CommentImage(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    image = ProcessedImageField(
        blank=True,
        upload_to=comment_img_path,
        processors=[ResizeToFit(1080, 720)],
        format='JPEG',
        options={'quality': 60},
        )