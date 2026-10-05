from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse
import urllib.parse
from .utils import generateOTP
from .models import UserOTPValidator, ViewerProfile, Movie, Genre, WatchHistory
import datetime
from django.contrib.auth.decorators import login_required
from .forms import ViewerProfileForm
import re
from .movie_n_series_script import main
from django.core.cache import cache
import time

@login_required(login_url="login")
def index(request):
    """
        Render the Home Page and sets the
        user profile data in the session upon successful login.
        Gets destroyed upon logout.
    """
    profile_id = request.GET.get('viewer_profile_id')
    portfolio_in_session = request.session.get("profile_id")
    if not portfolio_in_session:
        request.session['profile_id'] = profile_id
    return render(request, 'index.html')

def user_login(request):
    new_id = None
    if request.method == "POST":
        username = request.POST.get("email")
        password = request.POST.get("password")
        if not User.objects.filter(username=username).exists():
            messages.error(request, "Invalid username")
            return redirect("login")
        user = authenticate(username=username, password=password)
        if not user:
            messages.error(request, "Wrong Password")
            return redirect("login")
        # login(request, user)
        # return redirect("index")

        # not saving otp in the database keeping it in redis and destroy after sometime.
        generate_otp = generateOTP()
        print("user generated otp", generate_otp)
        cache.set(user.id, generate_otp, timeout=60)

        # generate_otp = generateOTP()
        # current_time = datetime.datetime.now() + datetime.timedelta(minutes=1)
        # new_id = UserOTPValidator.objects.create(user=user, otp=generate_otp, otp_expiry=current_time)

        # base_url = reverse('verifyOtp')
        # query_string = urllib.parse.urlencode({'id':new_id.id})
        # url = f"{base_url}?{query_string}"
        return redirect("verifyOtp", id=user.id)
    return render(request, 'login.html')

def verify_otp(request, id):
    context = {}
    user = User.objects.get(id = id)
    otp = cache.get(int(id))
    print("==cache otp==", otp)
    message_value = ""
    context["id"] = id
    if not otp:
        return redirect("login")
    if request.method == "POST":
        entered_otp = request.POST.get('otp')
        if entered_otp:
            if int(entered_otp) == int(otp):
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request, user)
                return redirect("profileList")
            else:
                message_value = "Wrong OTP"
        else:
            message_value = "Please enter a valid OTP"
        context["message"] = message_value
    return render(request, 'otp_verification.html', context)

def resend_otp(request, id):
    generate_otp = generateOTP()
    print("otp resend user generated otp", generate_otp)
    cache.set(int(id), generate_otp, timeout=60)
    return redirect("verifyOtp", id = int(id))

def user_logout(request):
    logout(request)
    return redirect("index")

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
            return redirect("index")
    messages.error(request, "Provide password satisfying the above checks.")
    return render(request, 'signup.html')

@login_required(login_url="login")
def create_profile(request):
    if request.method == "POST":
        form = ViewerProfileForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("profileList")
        else:
            errors = form.errors
            if errors:
                for error in list(errors.keys()):
                    error_val = re.sub(r'<[^<]+?>', '', str(errors[error]))
                    messages.error(request, f"* Profile Name : {error_val}")
    else:
        form = ViewerProfileForm()
    context = {
        'form': form,
    }
    return render(request, 'profileCreate.html', context)

@login_required(login_url="login")
def profile_list(request):
    user = request.user
    viewer_profiles = user.viewer_profile.all()
    context = {'viewer_profiles': viewer_profiles}
    return render(request, 'profileList.html', context)

@login_required(login_url="login")
def movie_list(request):
    search_string = request.POST.get("search-query")

    context = {}
    context["banner_movie"] = Movie.objects.order_by("-released").first()

    if search_string:
        search_string_in_cache = cache.get("search_string")

        # search and set cache
        if search_string_in_cache:
            context['new_movies'] = search_string_in_cache
        else:
            results = Movie.objects.filter(title__icontains = search_string)
            if results:
                context['new_movies'] = results
                cache.set("search_string", results, timeout=60)
            else:
                context["message"] = "NO Matching Movies Found"
    else:
        context["new_movies"] = Movie.objects.order_by("-released")[:8]
        context["only_on_netflix"] = Movie.objects.filter(only_on_netflix=True)
        action_record = Genre.objects.get(name="Action")
        context["actions"] = Movie.objects.filter(genre=action_record, movie_type="Movie")[:8]
    return render(request, 'movieList.html', context)

def movie_detail(request, uuid):
    movie = Movie.objects.get(uuid=uuid)
    actors = movie.actors.all()
    actors = ",".join([act.name for act in actors])
    directors = movie.directors.all()
    directors = ",".join([dic.name for dic in directors])
    movies_with_same_genre = Movie.objects.filter(genre__in=movie.genre.all()).distinct()[:8]
    context = {"movie": movie, "actors": actors, "directors": directors, "movies_with_same_genre": movies_with_same_genre}
    user_profile = ViewerProfile.objects.get(uuid=request.session.get("profile_id"))
    WatchHistory.objects.create(user=request.user, profile=user_profile, movie=movie)
    return render(request, 'movieDetail.html', context)

def sync_movies(request):
    print("calling Main")
    main()
    return render(request, 'movieList.html')