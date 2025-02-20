from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'home.html')

@login_required
def home_logged(request):
    return render(request, 'home_logged.html')
