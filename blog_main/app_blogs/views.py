from django.shortcuts import render, redirect
from .models import Category
from django.contrib.auth.models import User
from .forms import UserForm, CategoryForm, BlogForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
# Create your views here.

def home(request):
    categories = Category.objects.all()
    context = {"categories": categories}
    return render(request, 'home.html', context)

# check why not using csrf token causes security issues
def signup(request):
    categories = Category.objects.all()
    context = {"categories": categories}
    form = UserCreationForm()
    context['form'] = form
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():  # checks all the data provided is valid or not
            user = form.save()
            user.username = user.username.lower()
            form.save()
            login(request, user)
            return redirect("home")
    return render(request, 'signup.html', context)

def createCategory(request):
    form = CategoryForm()
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            print(category, "==category==")
            return redirect("home")
    return render(request, "category_form.html", {"form": form})


def createBlog(request):
    form = BlogForm()
    # if request.method == "POST":
    #     form = BlogForm(request.POST)
    return render(request, "blog_form.html")

