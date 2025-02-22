from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Add the home view as root URL
    path('home/', views.home_logged, name='home_logged'),  # Add URL pattern for logged-in homepage
    path('accounts/', include('allauth.urls')),  # This includes all the authentication URLs from allauth
    path('profile/', views.profile_view, name='profile'),  # Add URL pattern for user profile
    path('profile/edit/', views.edit_profile, name='edit_profile'),  # Add URL pattern for editing profile
]