from django.urls import path
from . import views

app_name = 'products'
urlpatterns = [
    path('', views.index, name='index'),
    path('create/',views.create, name='create'),
    path('<int:product_pk>/detail/',views.detail, name='detail'),
    path('<int:product_pk>/update/',views.update,name='update'),
    path('<int:product_pk>/delete/',views.delete,name='delete'),
    path('<int:product_pk>/likes/',views.likes,name='likes'),
    path('<int:product_pk>/review_create/',views.review_create, name='review_create'),
]