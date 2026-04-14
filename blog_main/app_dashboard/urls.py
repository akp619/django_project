from django.urls import path, include
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard_home, name='dashboard_home'),
    path('dashboard/<str:model>', views.fetch_models_data, name='modelData'),
]

