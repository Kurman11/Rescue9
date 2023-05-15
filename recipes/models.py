from django.db import models
from django.conf import settings
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import Thumbnail, ResizeToFit, ResizeToFill
from django_ckeditor_5.fields import CKEditor5Field
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.
def review_img_path(instance, filename):
    return f'images/review/{instance.review.user.username}/{filename}'

def recipe_thumbnail_path(instance, filename):
    return f'images/recipe/thumbnail/{instance.title}/{filename}'


class Recipe(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=20)
    thumbnail_upload = models.ImageField(upload_to=recipe_thumbnail_path)
    thumbnail = ImageSpecField(
        source = 'thumbnail_upload',
        processors = [Thumbnail(300, 300)],
        format='JPEG',
        options={'quality': 60},
        )
    
    thumbnail_crop = models.ImageField(upload_to='thumbnail_crop')

    category = models.CharField(max_length=20)
    hits = models.PositiveIntegerField(default=0)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="like_recipes")
    content = CKEditor5Field('Content', config_name='extends')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    used_products = models.ManyToManyField("products.Product", related_name="used_recipes", blank=True)

    def __srt__(self):
        return self.title


class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    content = models.TextField()
    like_user = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="like_reviews")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = ProcessedImageField(
        blank=True,
        upload_to=review_img_path,
        processors=[ResizeToFit(1080, 720)],
        format='JPEG',
        options={'quality': 60},
        )
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    