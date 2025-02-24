from allauth.account.forms import SignupForm
from django import forms
from django.contrib.auth import get_user_model
from .models import UserProfile, Antecedentes, DadosBiometricos
from medical_records.models import MedicamentoAnvisa

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
        # Create UserProfile if it doesn't exist
        UserProfile.objects.get_or_create(user=user)
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

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            # Update UserProfile fields
            profile = user.userprofile
            profile.phone_number = self.cleaned_data.get('phone_number')
            profile.street = self.cleaned_data.get('street')
            profile.number = self.cleaned_data.get('number')
            profile.neighborhood = self.cleaned_data.get('neighborhood')
            profile.zip_code = self.cleaned_data.get('zip_code')
            profile.city = self.cleaned_data.get('city')
            profile.state = self.cleaned_data.get('state')
            profile.date_of_birth = self.cleaned_data.get('date_of_birth')
            profile.sex = self.cleaned_data.get('sex')
            profile.marital_status = self.cleaned_data.get('marital_status')
            profile.profession = self.cleaned_data.get('profession')
            profile.race_ethnicity = self.cleaned_data.get('race_ethnicity')
            profile.nationality = self.cleaned_data.get('nationality')
            profile.emergency_contact_name = self.cleaned_data.get('emergency_contact_name')
            profile.emergency_contact_phone = self.cleaned_data.get('emergency_contact_phone')
            profile.emergency_contact_relationship = self.cleaned_data.get('emergency_contact_relationship')
            profile.education_level = self.cleaned_data.get('education_level')
            profile.religion = self.cleaned_data.get('religion')
            profile.sus_card_number = self.cleaned_data.get('sus_card_number')
            profile.health_insurance = self.cleaned_data.get('health_insurance')
            profile.save()
        return user
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
    medications = forms.ModelMultipleChoiceField(
        queryset=MedicamentoAnvisa.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        label='Medicações em Uso'
    )
    allergies = forms.ModelMultipleChoiceField(
        queryset=MedicamentoAnvisa.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        label='Alergias'
    )

    class Meta:
        model = Antecedentes
        fields = ['doencas_cronicas', 'cirurgias', 'historico_familiar', 'habitos', 'medications', 'allergies']
        widgets = {
            'doencas_cronicas': forms.Textarea(attrs={'rows': 3}),
            'cirurgias': forms.Textarea(attrs={'rows': 3}),
            'historico_familiar': forms.Textarea(attrs={'rows': 3}),
            'habitos': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.profile:
            self.fields['medications'].initial = self.instance.profile.medications.all()
            self.fields['allergies'].initial = self.instance.profile.allergies.all()

    def save(self, commit=True):
        antecedentes = super().save(commit=False)
        if commit:
            antecedentes.save()
            if antecedentes.profile:
                antecedentes.profile.medications.set(self.cleaned_data['medications'])
                antecedentes.profile.allergies.set(self.cleaned_data['allergies'])
        return antecedentes
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