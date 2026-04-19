from django.urls import path
from . import views
urlpatterns = [
    path('user-login/', views.userLogin, name="userLogin"),
    path('user-register/', views.userRegister, name="userRegister"),
    path('update-user-profile/<str:pk>', views.userProfileUpdate, name="userProfileUpdate"),
    path('user-logout/', views.userLogout, name="userLogout"),
    path('', views.home, name="home"),
    path('room/<str:pk>', views.room, name="room"), # pass a primary key for the room
    path('user/<str:pk>', views.userProfile, name="userProfile"), # pass a primary key for the user
    path('create-room/', views.createRoom, name="createRoom"),
    path('update-room/<str:pk>', views.updateRoom, name="updateRoom"),
    path('delete-room/<str:pk>', views.delete, name="deleteRoom"),
    path('delete-message/<str:pk>/<str:room_pk>', views.deleteMessage, name="deleteMessage")
]
