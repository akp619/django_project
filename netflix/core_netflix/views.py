from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse
import urllib.parse
from .utils import generateOTP
from .models import UserOTPValidator
import datetime


def index(request):
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
        generate_otp = generateOTP()
        current_time = datetime.datetime.now() + datetime.timedelta(minutes=1)
        new_id = UserOTPValidator.objects.create(user=user, otp=generate_otp, otp_expiry=current_time)
        # base_url = reverse('verifyOtp')
        # query_string = urllib.parse.urlencode({'id':new_id.id})
        # url = f"{base_url}?{query_string}"
        return redirect("verifyOtp", id=new_id.id)
    return render(request, 'login.html')

def verify_otp(request, id):
    print("==id==", id)
    otp_id = UserOTPValidator.objects.get(id = id)
    if not otp_id:
        return redirect("login")
    if request.method == "POST":
        otp = request.POST.get('otp')
        if int(otp) == int(otp_id.otp):
            login(request, otp_id.user)
            return redirect("index")
        return redirect("verifyOtp", id)
    return render(request, 'otp_verification.html', {'id': id})


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