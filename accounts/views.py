from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from .forms import UserEditForm
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
        # Calculate age if date_of_birth is available
        age = None
        if hasattr(request.user, 'userprofile') and request.user.userprofile.date_of_birth:
            from datetime import date
            dob = request.user.userprofile.date_of_birth
            today = date.today()
            age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        
        return render(request, 'account/profile.html', {'age': age})
    except Exception as e:
        logger.error(f'Error rendering profile page for user {request.user.username}: {str(e)}')
        messages.error(request, 'Ocorreu um erro ao carregar a página de perfil. Por favor, tente novamente.')
        return redirect(reverse('home_logged'))

@login_required
def edit_profile(request):
    logger.info(f'User {request.user.username} accessing edit profile page')
    try:
        if request.method == 'POST':
            form = UserEditForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                messages.success(request, 'Perfil atualizado com sucesso!')
                return redirect('profile')
        else:
            form = UserEditForm(instance=request.user)
        return render(request, 'account/edit_profile.html', {'form': form})
    except Exception as e:
        logger.error(f'Error in edit profile for user {request.user.username}: {str(e)}')
        messages.error(request, 'Ocorreu um erro ao editar o perfil. Por favor, tente novamente.')
        return redirect('profile')
