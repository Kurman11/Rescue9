from django.urls import path
from recipes import views

app_name = "recipes"
urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    path('<int:recipe_pk>/', views.detail, name='detail'),
    path('<int:recipe_pk>/update/', views.update, name='update'),
]