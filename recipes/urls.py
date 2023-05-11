from django.urls import path
from recipes import views

app_name = "recipes"
urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    path('<int:recipe_pk>/', views.detail, name='detail'),
    path('<int:recipe_pk>/update/', views.update, name='update'),
    path('<int:recipe_pk>/delete/', views.delete, name='delete'),
    path('<int:recipe_pk>/like/', views.recipe_like, name='recipe_like'),
    path('category/<str:subject>/', views.category, name='category'),
    path('<int:recipe_pk>/comments', views.comment_create, name='comment_create'),
    path('<int:recipe_pk>/comments/<int:comment_pk>/update/', views.comment_update, name='comment_update'),
    path('<int:recipe_pk>/comments/<int:comment_pk>/delete/', views.comment_delete, name='comment_delete'),
    path('<int:recipe_pk>/comments/<int:comment_pk>/like/', views.comment_like, name='comment_like'),
    path("image_upload/", views.upload_file, name="ck_editor_5_upload_file"),
]