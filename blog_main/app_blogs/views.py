from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Blog, About, SocialLinks
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import UserForm, CategoryForm, BlogForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q  # this is used for "OR" filter
from django.apps import apps
from django.http import HttpResponse, HttpResponseRedirect
# Create your views here.

def home(request):
    # categories = Category.objects.all()
    #"filter" is used to filter out records and "slicing [:]" is used to limit the number of records.
    featured_blogs = Blog.objects.filter(is_featured=True).order_by('-created')
    blogs = Blog.objects.filter(is_featured=False).order_by('-created')
    print(blogs, "==blogs==")
    context = {"blogs": blogs, "featured_blogs": featured_blogs}
    if request.GET.get("parameter"):
        context["parameter"] = request.GET["parameter"]
        searched_blogs = Blog.objects.filter(Q(title__icontains= request.GET['parameter']) | Q(blog_body__icontains = request.GET['parameter']) )
        print(searched_blogs, "==searched blogs==")
    return render(request, 'home.html', context)

# check why not using csrf token causes security issues

#Just for Note:- Instead of using custom forms we can django crispy forms or django default forms
def signup(request):
    context = {}
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

def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        #  check for valid username
        if not User.objects.filter(username=username).exists():
            messages.error(request, "Invalid username")
            return redirect("login")
        user = authenticate(username=username, password=password)

        if not user:
            messages.error(request, "Wrong Password.")
            return redirect("login")

        login(request, user)
        return redirect("home")

    return render(request, "login.html")

def user_logout(request):
    logout(request)
    return redirect("login")

def createCategory(request):
    form = CategoryForm()
    type = 'create'
    if request.method == "POST":
        print(request.POST, "diwjdiwjodiwdiwjdowi")
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            print(category, "==category==")
            return redirect("home")
    return render(request, "category_form.html", {"form": form, 'type': type})

def editCategory(request, category_id):
    category = Category.objects.get(id=category_id)
    form = CategoryForm(instance=category)
    type = 'edit'

    if request.method == 'POST':
        category.description = request.POST['description']
        category.save()
        return redirect('modelData', model="Category")

    context = {'form': form, 'category': category, 'type': type}
    return render(request, 'category_form.html', context)

def createBlog(request):
    type = 'create'
    category = Category.objects.all()
    status = Blog._meta.get_field('status').choices
    author = User.objects.all()

    # request.POST [data to create record] > request.FILES [create files]
    form = BlogForm(request.POST, request.FILES)
    if form.is_valid():
        form.save()
        return redirect("home")

    # custom way to create a new record.

    # if request.method == "POST":
    #     create_or_existing_category = Category.objects.get_or_create(name=request.POST.get("category"))
    #     create_or_existing_author = User.objects.get_or_create(username=request.POST.get("author"))
    #     new_blog = Blog.objects.create(
    #         title=request.POST.get("title"),
    #         short_description=request.POST.get("short_description"),
    #         slug = request.POST.get("short_description").replace("","-"),
    #         blog_body=request.POST.get("blog_body"),
    #         status = 0,
    #         is_featured = True,
    #         category = create_or_existing_category[0],
    #         author = create_or_existing_author[0],
    #     )
    #     return redirect("modelData", model = Blog.__name__)
    context = {'category': category, 'author': author, 'form': form, 'status': status, 'type': type}
    return render(request, "blog_form.html", context)

def editBlog(request, blog_id):
    type = 'edit'
    form = BlogForm()
    category = Category.objects.all()
    status = Blog._meta.get_field('status').choices
    author = User.objects.all()
    blog = Blog.objects.get(id=blog_id)
    if request.method == "POST":
        form = BlogForm(request.POST, instance=blog)
        if form.is_valid():
            form.save()
    context = {'category': category, 'author': author, 'form': form, 'status': status, 'type': type, 'blog': blog}
    return render(request, "blog_form.html", context)

def deleteBlog(request, model, id):
    MyModel = apps.get_model(app_label='app_blogs', model_name=model)
    get_record_data = MyModel.objects.get(id=id)
    form = BlogForm(instance=get_record_data)
    context = {'model': MyModel.__name__, 'id':get_record_data.id, 'form':form}
    if request.method == "POST":
        get_record_data.delete()
        return redirect("modelData", model=MyModel.__name__)
    return render(request, "delete_record.html", context)

@login_required(login_url='login') #parameter "login_url" will redirect to login page is user access a unauthorized page.
def categoryBlogs(request, category_id):
    if category_id:
        try:
            category_id = Category.objects.get(pk=category_id)
        except:
            category = get_object_or_404(Category, pk=category_id)
            return category
        blogs = Blog.objects.filter(category_id=category_id)
        if blogs:
            context = {"blogs": blogs}
            # context['categories'] = Category.objects.all()
            return render(request, "category_blogs.html", context)

def blogPost(request,slug):
    post = get_object_or_404(Blog, slug=slug)
    return render(request, "blog_post.html", {"post": post})

def about(request):
    about = About.objects.all()
    return render(request, 'blog_about.html', {"about": about})

