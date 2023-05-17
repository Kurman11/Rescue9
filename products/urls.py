from django.urls import path
from . import views

app_name = 'products'
urlpatterns = [
    path('', views.index, name='index'),
    path('category/<str:category>/', views.filter_products, name='filter_products'),
    path('create/',views.create, name='create'),
    path('<int:product_pk>/',views.detail, name='detail'),
    path('<int:product_pk>/update/',views.update,name='update'),
    path('<int:product_pk>/delete/',views.delete,name='delete'),
    path('<int:product_pk>/likes/',views.likes,name='likes'),
    path('<int:product_pk>/comment_create/',views.comment_create, name='comment_create'),
    path('<int:product_pk>/comments/<int:comment_pk>/comment_update/',views.comment_update, name='comment_update'),
    path('<int:product_pk>/comments/<int:comment_pk>/comment_delete/',views.comment_delete, name='comment_delete'),
    path('<int:product_pk>/comments/<int:comment_pk>/comment_likes/',views.comment_likes, name='comment_likes'),
]

