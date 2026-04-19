from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('sign-up/', views.signup, name="signup"),
    path('login/', views.user_login, name="login"),
    path('logout/', views.user_logout, name="logout"),
    path('create-category/', views.createCategory, name="createCategory"),
    path('edit-category/<int:category_id>', views.editCategory, name="editCategory"),
    path('create-blog/', views.createBlog, name="createBlog"),
    path('edit-blog/<int:blog_id>', views.editBlog, name="editBlog"),
    path('create-user/', views.createUser, name="createUser"),
    path('edit-user/<int:user_id>', views.editUser, name="editUser"),
    path('delete/<str:model>/<int:id>', views.deleteBlog, name="deleteData"),
    path('category/<int:category_id>', views.categoryBlogs, name="categoryBlogs"),
    path('about/', views.about, name="about"),
    path('blog/<str:slug>/', views.blogPost, name="blogPost"),
]