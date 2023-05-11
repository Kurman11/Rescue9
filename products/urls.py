from django.urls import path
from . import views

app_name = 'products'
urlpatterns = [
    path('', views.index, name='index'),
    path('create/',views.create, name='create'),
    path('<int:product_pk>/',views.detail, name='detail'),
    path('<int:product_pk>/update/',views.update,name='update'),
    path('<int:product_pk>/delete/',views.delete,name='delete'),
    path('<int:product_pk>/likes/',views.likes,name='likes'),
    path('<int:product_pk>/review_create/',views.review_create, name='review_create'),
    path('<int:product_pk>/reviews/<int:review_pk>/review_update',views.review_update, name='review_update'),
    path('<int:product_pk>/reviews/<int:review_pk>/review_delete',views.review_delete, name='review_delete'),
    path('<int:product_pk>/reviews/<int:review_pk>/review_likes',views.review_likes, name='review_likes'),
]