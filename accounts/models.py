from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_doctor = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=20, blank=True)
    # Detailed address fields
    street = models.CharField(max_length=255, blank=True, verbose_name="Rua")
    number = models.CharField(max_length=20, blank=True, verbose_name="Número")
    neighborhood = models.CharField(max_length=100, blank=True, verbose_name="Bairro")
    zip_code = models.CharField(max_length=9, blank=True, verbose_name="CEP")
    city = models.CharField(max_length=100, blank=True, verbose_name="Cidade")
    state = models.CharField(max_length=2, blank=True, verbose_name="Estado")
    # Personal information
    date_of_birth = models.DateField(null=True, blank=True)
    sex = models.CharField(max_length=10, choices=[("M", "Masculino"), ("F", "Feminino"), ("O", "Outro")], blank=True)
    marital_status = models.CharField(max_length=20, choices=[("solteiro", "Solteiro(a)"), ("casado", "Casado(a)"), ("divorciado", "Divorciado(a)"), ("viuvo", "Viúvo(a)")], blank=True)
    profession = models.CharField(max_length=100, blank=True, verbose_name="Profissão")
    race_ethnicity = models.CharField(max_length=50, choices=[
        ("branca", "Branca"),
        ("preta", "Preta"),
        ("parda", "Parda"),
        ("amarela", "Amarela"),
        ("indigena", "Indígena")
    ], blank=True, verbose_name="Raça/Etnia")
    nationality = models.CharField(max_length=100, blank=True, verbose_name="Nacionalidade")
    # Emergency contact
    emergency_contact_name = models.CharField(max_length=100, blank=True, verbose_name="Nome do Contato de Emergência")
    emergency_contact_phone = models.CharField(max_length=20, blank=True, verbose_name="Telefone do Contato de Emergência")
    emergency_contact_relationship = models.CharField(max_length=50, blank=True, verbose_name="Parentesco do Contato de Emergência")
    # Education and health information
    education_level = models.CharField(max_length=50, choices=[
        ("fundamental_incompleto", "Fundamental Incompleto"),
        ("fundamental_completo", "Fundamental Completo"),
        ("medio_incompleto", "Médio Incompleto"),
        ("medio_completo", "Médio Completo"),
        ("superior_incompleto", "Superior Incompleto"),
        ("superior_completo", "Superior Completo"),
        ("pos_graduacao", "Pós-graduação")
    ], blank=True, verbose_name="Grau de Instrução")
    religion = models.CharField(max_length=100, blank=True, verbose_name="Religião/Crença")
    sus_card_number = models.CharField(max_length=15, blank=True, verbose_name="Número do Cartão SUS")
    health_insurance = models.CharField(max_length=100, blank=True, verbose_name="Convênio/Plano de Saúde")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

class Antecedentes(models.Model):
    profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, primary_key=True)
    historico_familiar = models.TextField(null=True, blank=True, verbose_name='Histórico Familiar')
    alergias = models.TextField(null=True, blank=True, verbose_name='Alergias')
    doencas_cronicas = models.TextField(null=True, blank=True, verbose_name='Doenças Crônicas')
    cirurgias = models.TextField(null=True, blank=True, verbose_name='Cirurgias Anteriores')
    medicamentos = models.TextField(null=True, blank=True, verbose_name='Medicamentos em Uso')

    def __str__(self):
        return f"Antecedentes de {self.profile}"

    class Meta:
        verbose_name = 'Antecedente'
        verbose_name_plural = 'Antecedentes'

class DadosBiometricos(models.Model):
    profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, primary_key=True)
    altura = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name='Altura (m)')
    peso = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name='Peso (kg)')
    pressao_arterial = models.CharField(max_length=20, null=True, blank=True, verbose_name='Pressão Arterial')
    tipo_sanguineo = models.CharField(max_length=5, null=True, blank=True, verbose_name='Tipo Sanguíneo')

    def __str__(self):
        return f"Dados Biométricos de {self.profile}"

    class Meta:
        verbose_name = 'Dados Biométricos'
        verbose_name_plural = 'Dados Biométricos'

    @property
    def imc(self):
        if self.altura and self.peso:
            altura_m = float(self.altura)
            peso_kg = float(self.peso)
            if altura_m > 0:
                return round(peso_kg / (altura_m * altura_m), 2)
        return None

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()

@receiver(post_save, sender=UserProfile)
def create_related_models(sender, instance, created, **kwargs):
    if created:
        Antecedentes.objects.create(profile=instance)
        DadosBiometricos.objects.create(profile=instance)
