from django.db import models
from django.conf import settings
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from imagekit.models import ImageSpecField
from imagekit.processors import Thumbnail
# Create your models here.

def product_img_path(instance, filename):
    return f'images/product/{instance.name}/{filename}'

class Product(models.Model):
    name = models.CharField(max_length=50)
    category = models.CharField(max_length=20)
    hits = models.PositiveIntegerField(default=0)
    photo = models.ImageField(upload_to=product_img_path)
    Thumbnail = ImageSpecField( 
		source = 'photo', 		   # 원본 ImageField 명
		processors = [Thumbnail(300, 300)], # 처리할 작업목록
		format = 'JPEG',		   # 최종 저장 포맷
		options = {'quality': 90}) # 저장 옵션
    
    # tage = 

    is_new = models.BooleanField(default=False)
    content = models.TextField()
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_product',null=True)


class Review(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, blank=False, null=False, on_delete=models.CASCADE)
    crated_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    content = models.CharField(max_length=600)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_review',null=True)
    rating = models.FloatField()

class Review_image(models.Model):
    review_id = models.ForeignKey(Review,blank=False, null=False, on_delete=models.CASCADE)
    image = ProcessedImageField(blank = True, 
                                null= True, 
                                upload_to='review/', 
                                processors=[ResizeToFill(300, 300)], 
                                format = 'JPEG', 
                                options={'quality': 90},)
