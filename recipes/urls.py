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
    path('<int:recipe_pk>/reviews', views.review_create, name='review_create'),
    path('<int:recipe_pk>/reviews/<int:review_pk>/review_update/', views.review_update, name='review_update'),
    path('<int:recipe_pk>/reviews/<int:review_pk>/review_delete/', views.review_delete, name='review_delete'),
    path('<int:recipe_pk>/reviews/<int:review_pk>/like/', views.review_like, name='review_like'),
]