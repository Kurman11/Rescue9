from django.db import models
from django.contrib.auth.models import AbstractUser
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import Thumbnail, ResizeToFit



# Create your models here.
class User(AbstractUser):
    nickname = models.CharField(max_length=20)
    image = ProcessedImageField(upload_to='users', 
                                blank=True,
                                processors=[Thumbnail(100,100)],
                                format='JPEG',
                                options={'quality': 80})