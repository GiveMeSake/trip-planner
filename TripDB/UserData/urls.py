from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('join', views.join, name="join"),
    path('home', views.home, name="home"),  # Add this line to handle /home URL
    #path('add_post', views.add_path, name="add_post"),
]
