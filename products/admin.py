from django.contrib import admin
from .models import Product, Review, Review_image

# Register your models here.
admin.site.register(Product)
admin.site.register(Review)
admin.site.register(Review_image)