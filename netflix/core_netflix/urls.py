from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name="index"),
    path('login/', views.user_login, name="login"),
    path('otp-verification/<int:id>/', views.verify_otp, name="verifyOtp"),
    path('sign-up/', views.signup, name="signup"),
]
