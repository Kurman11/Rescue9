from django.urls import path
from recipes import views

app_name = "recipes"
urlpatterns = [
    path('', views.index, name='recipes_index'),
]