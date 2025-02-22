from allauth.account.forms import SignupForm
from django import forms
from django.contrib.auth import get_user_model
from .models import UserProfile

class CustomSignupForm(SignupForm):
    username = forms.CharField(max_length=30, label='Nome de Usuário')
    first_name = forms.CharField(max_length=30, label='Nome')
    last_name = forms.CharField(max_length=30, label='Sobrenome')
    
    def save(self, request):
        user = super().save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.username = self.cleaned_data['username']
        user.save()
        return user

class UserEditForm(forms.ModelForm):
    phone_number = forms.CharField(max_length=20, required=False, label='Telefone')
    address = forms.CharField(widget=forms.Textarea, required=False, label='Endereço')
    date_of_birth = forms.DateField(required=False, label='Data de Nascimento', 
                                  widget=forms.DateInput(attrs={'type': 'date'}))
    is_doctor = forms.BooleanField(required=False, label='É médico?')

    class Meta:
        model = get_user_model()
        fields = ['username', 'first_name', 'last_name', 'email']
        labels = {
            'username': 'Nome de Usuário',
            'first_name': 'Nome',
            'last_name': 'Sobrenome',
            'email': 'Email'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and hasattr(self.instance, 'userprofile'):
            self.fields['phone_number'].initial = self.instance.userprofile.phone_number
            self.fields['address'].initial = self.instance.userprofile.address
            self.fields['date_of_birth'].initial = self.instance.userprofile.date_of_birth
            self.fields['is_doctor'].initial = self.instance.userprofile.is_doctor

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            # Update UserProfile
            profile = user.userprofile
            profile.phone_number = self.cleaned_data['phone_number']
            profile.address = self.cleaned_data['address']
            profile.date_of_birth = self.cleaned_data['date_of_birth']
            profile.is_doctor = self.cleaned_data['is_doctor']
            profile.save()
        return user