from django.db import models
from django.conf import settings
from imagekit.models import ImageSpecField
from imagekit.processors import Thumbnail
from taggit.managers import TaggableManager
# Create your models here.

def product_img_path(instance, filename):
    return f'images/product/{instance.name}/{filename}'

class ConvenienceStore(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name
    

class Product(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    price = models.IntegerField(default=0)
    category = models.CharField(max_length=20)
    hits = models.PositiveIntegerField(default=0)
    photo = models.ImageField(upload_to=product_img_path)
    Thumbnail = ImageSpecField( 
		source = 'photo', 		   # 원본 ImageField 명
		processors = [Thumbnail(300, 300)], # 처리할 작업목록
		format = 'JPEG',		   # 최종 저장 포맷
		options = {'quality': 90}) # 저장 옵션
    tags = TaggableManager(blank=True)
    is_new = models.BooleanField(default=False)
    content = models.TextField()
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_product')
    convenience_stores = models.ManyToManyField(ConvenienceStore)

    def __str__(self):
        return self.name



class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, blank=False, null=False, on_delete=models.CASCADE)
    crated_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    content = models.CharField(max_length=600)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_comment')
