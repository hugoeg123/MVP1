from allauth.account.forms import SignupForm
from django import forms
from django.contrib.auth import get_user_model
from .models import UserProfile, Antecedentes, DadosBiometricos

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
    # Registration Information
    username = forms.CharField(max_length=30, label='Nome de Usuário')
    first_name = forms.CharField(max_length=30, label='Nome')
    last_name = forms.CharField(max_length=30, label='Sobrenome')
    email = forms.EmailField(label='Email')
    
    # Contact Information
    phone_number = forms.CharField(max_length=20, required=False, label='Celular')
    emergency_contact_name = forms.CharField(max_length=100, required=False, label='Nome do Contato de Emergência')
    emergency_contact_phone = forms.CharField(max_length=20, required=False, label='Telefone do Contato de Emergência')
    emergency_contact_relationship = forms.CharField(max_length=50, required=False, label='Parentesco do Contato de Emergência')
    
    # Address Information
    street = forms.CharField(max_length=255, required=False, label='Rua')
    number = forms.CharField(max_length=20, required=False, label='Número')
    neighborhood = forms.CharField(max_length=100, required=False, label='Bairro')
    zip_code = forms.CharField(max_length=9, required=False, label='CEP')
    city = forms.CharField(max_length=100, required=False, label='Cidade')
    state = forms.CharField(max_length=2, required=False, label='Estado')
    
    # Demographic Information
    date_of_birth = forms.DateField(required=False, label='Data de Nascimento', 
                                  widget=forms.DateInput(attrs={'type': 'date'}))
    sex = forms.ChoiceField(choices=[("",'Selecione'),("M", "Masculino"), ("F", "Feminino"), ("O", "Outro")], required=False, label='Sexo')
    marital_status = forms.ChoiceField(choices=[("solteiro", "Solteiro(a)"), ("casado", "Casado(a)"), ("divorciado", "Divorciado(a)"), ("viuvo", "Viúvo(a)")], required=False, label='Estado Civil')
    profession = forms.CharField(max_length=100, required=False, label='Profissão')
    race_ethnicity = forms.ChoiceField(choices=[
        ("branca", "Branca"),
        ("preta", "Preta"),
        ("parda", "Parda"),
        ("amarela", "Amarela"),
        ("indigena", "Indígena")
    ], required=False, label='Raça/Etnia')
    nationality = forms.CharField(max_length=100, required=False, label='Nacionalidade')
    # Emergency contact
    emergency_contact_name = forms.CharField(max_length=100, required=False, label='Nome do Contato de Emergência')
    emergency_contact_phone = forms.CharField(max_length=20, required=False, label='Telefone do Contato de Emergência')
    emergency_contact_relationship = forms.CharField(max_length=50, required=False, label='Parentesco do Contato de Emergência')
    # Education and health information
    education_level = forms.ChoiceField(
        choices=[
            ('', 'Selecione'),
            ("fundamental_incompleto", "Fundamental Incompleto"),
            ("fundamental_completo", "Fundamental Completo"),
            ("medio_incompleto", "Médio Incompleto"),
            ("medio_completo", "Médio Completo"),
            ("superior_incompleto", "Superior Incompleto"),
            ("superior_completo", "Superior Completo"),
            ("pos_graduacao", "Pós-graduação")
        ],
        required=False,
        label='Grau de Instrução'
    )
    religion = forms.CharField(max_length=100, required=False, label='Religião/Crença')
    sus_card_number = forms.CharField(max_length=15, required=False, label='Número do Cartão SUS')
    health_insurance = forms.CharField(max_length=100, required=False, label='Convênio/Plano de Saúde')

    class Meta:
        model = get_user_model()
        fields = ['username', 'first_name', 'last_name', 'email']
        labels = {
            'username': 'Nome de Usuário',
            'first_name': 'Nome',
            'last_name': 'Sobrenome',
            'email': 'Email'
        }
        help_texts = {
            'username': ''
        }

class AntecedentesForm(forms.ModelForm):
    class Meta:
        model = Antecedentes
        fields = ['historico_familiar', 'alergias', 'doencas_cronicas', 'cirurgias', 'medicamentos']
        widgets = {
            'historico_familiar': forms.Textarea(attrs={'rows': 3}),
            'alergias': forms.Textarea(attrs={'rows': 3}),
            'doencas_cronicas': forms.Textarea(attrs={'rows': 3}),
            'cirurgias': forms.Textarea(attrs={'rows': 3}),
            'medicamentos': forms.Textarea(attrs={'rows': 3}),
        }

class DadosBiometricosForm(forms.ModelForm):
    class Meta:
        model = DadosBiometricos
        fields = ['altura', 'peso', 'pressao_arterial', 'tipo_sanguineo']
        widgets = {
            'altura': forms.NumberInput(attrs={'step': '0.01', 'min': '0', 'max': '3'}),
            'peso': forms.NumberInput(attrs={'step': '0.1', 'min': '0', 'max': '500'}),
            'pressao_arterial': forms.TextInput(attrs={'placeholder': 'Ex: 120/80'}),
            'tipo_sanguineo': forms.Select(choices=[
                ('', 'Selecione'),
                ('A+', 'A+'), ('A-', 'A-'),
                ('B+', 'B+'), ('B-', 'B-'),
                ('AB+', 'AB+'), ('AB-', 'AB-'),
                ('O+', 'O+'), ('O-', 'O-'),
            ])
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