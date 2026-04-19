from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import Category, Blog

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = "__all__"
        exclude = ('last_login', 'is_superuser', 'user_permissions', 'date_joined', 'password')


class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ["name", "description", ]


class BlogForm(ModelForm):
    class Meta:
        model = Blog
        fields = "__all__"
        exclude = ('created', 'updated', 'slug')