from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('sign-up/', views.signup, name="signup"),
    path('create-category/', views.createCategory, name="createCategory"),
    path('create-blog/', views.createBlog, name="createBlog"),
]