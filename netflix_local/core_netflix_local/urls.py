from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name="index"),
    path('login/', views.user_login, name="login"),
    path('logout/', views.user_logout, name="logout"),
    path('otp-verification/<int:id>/', views.verify_otp, name="verifyOtp"),
    path('resend-otp/<int:id>/', views.resend_otp, name="ResendOtp"),
    path('sign-up/', views.signup, name="signup"),
    path('profile-create/', views.create_profile, name="createProfile"),
    path('profile-list/', views.profile_list, name="profileList"),
    path('movie-list/', views.movie_list, name="movieList"),
    path('sync-movie/', views.sync_movies, name="syncMovies"),
    path('movie-detail/<str:uuid>', views.movie_detail, name="movieDetail"),
]
