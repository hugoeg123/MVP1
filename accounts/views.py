from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
import logging

# Configure logging
logger = logging.getLogger(__name__)

def home(request):
    if request.user.is_authenticated:
        logger.info(f'Authenticated user {request.user.username} accessing home page')
        return redirect('home_logged')
    return render(request, 'home.html')

@login_required
def home_logged(request):
    logger.info(f'User {request.user.username} accessing home_logged page')
    try:
        return render(request, 'home_logged.html')
    except Exception as e:
        logger.error(f'Error rendering home_logged page for user {request.user.username}: {str(e)}')
        messages.error(request, 'Ocorreu um erro ao carregar a página. Por favor, tente novamente.')
        return redirect(reverse('home'))

@login_required
def profile_view(request):
    logger.info(f'User {request.user.username} accessing profile page')
    try:
        return render(request, 'account/profile.html')
    except Exception as e:
        logger.error(f'Error rendering profile page for user {request.user.username}: {str(e)}')
        messages.error(request, 'Ocorreu um erro ao carregar a página de perfil. Por favor, tente novamente.')
        return redirect(reverse('home_logged'))
