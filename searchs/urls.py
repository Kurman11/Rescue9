from django.urls import path
from . import views

app_name = "searchs"

urlpatterns = [
    path('search/',views.search, name='search'),
]
