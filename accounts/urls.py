from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Add the home view as root URL
    path('accounts/', include('allauth.urls')),  # This includes all the authentication URLs from allauth
]