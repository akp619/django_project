from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import Category, Blog

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = "__all__"
        exclude = ('password', 'last_login', 'is_superuser', 'groups', 'user_permissions', 'username', 'is_staff', 'is_active', 'date_joined')


class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ["name", "description", ]


class BlogForm(ModelForm):
    class Meta:
        model = Blog
        fields = "__all__"
        exclude = ('created', 'updated', 'slug')