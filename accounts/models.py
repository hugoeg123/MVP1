from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from medical_records.models import MedicamentoAnvisa

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_doctor = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=20, null=True, blank=True, default=None)
    # Medications and Allergies
    medications = models.ManyToManyField(MedicamentoAnvisa, related_name='user_medications', blank=True)
    allergies = models.ManyToManyField(MedicamentoAnvisa, related_name='user_allergies', blank=True)
    # Detailed address fields
    street = models.CharField(max_length=255, null=True, blank=True, verbose_name="Rua")
    number = models.CharField(max_length=20, null=True, blank=True, verbose_name="Número")
    neighborhood = models.CharField(max_length=100, null=True, blank=True, verbose_name="Bairro")
    zip_code = models.CharField(max_length=9, null=True, blank=True, verbose_name="CEP")
    city = models.CharField(max_length=100, null=True, blank=True, verbose_name="Cidade")
    state = models.CharField(max_length=2, null=True, blank=True, verbose_name="Estado")
    # Personal information
    date_of_birth = models.DateField(null=True, blank=True)
    sex = models.CharField(max_length=10, null=True, choices=[("M", "Masculino"), ("F", "Feminino"), ("O", "Outro")], blank=True)
    marital_status = models.CharField(max_length=20, null=True, choices=[("solteiro", "Solteiro(a)"), ("casado", "Casado(a)"), ("divorciado", "Divorciado(a)"), ("viuvo", "Viúvo(a)")], blank=True)
    profession = models.CharField(max_length=100, null=True, blank=True, verbose_name="Profissão")
    race_ethnicity = models.CharField(max_length=50, null=True, choices=[
        ("branca", "Branca"),
        ("preta", "Preta"),
        ("parda", "Parda"),
        ("amarela", "Amarela"),
        ("indigena", "Indígena")
    ], blank=True, verbose_name="Raça/Etnia")
    nationality = models.CharField(max_length=100, null=True, blank=True, verbose_name="Nacionalidade")
    # Emergency contact
    emergency_contact_name = models.CharField(max_length=100, null=True, blank=True, verbose_name="Nome do Contato de Emergência")
    emergency_contact_phone = models.CharField(max_length=20, null=True, blank=True, verbose_name="Telefone do Contato de Emergência")
    emergency_contact_relationship = models.CharField(max_length=50, null=True, blank=True, verbose_name="Parentesco do Contato de Emergência")
    # Education and health information
    education_level = models.CharField(max_length=50, null=True, choices=[
        ("fundamental_incompleto", "Fundamental Incompleto"),
        ("fundamental_completo", "Fundamental Completo"),
        ("medio_incompleto", "Médio Incompleto"),
        ("medio_completo", "Médio Completo"),
        ("superior_incompleto", "Superior Incompleto"),
        ("superior_completo", "Superior Completo"),
        ("pos_graduacao", "Pós-graduação")
    ], blank=True, verbose_name="Grau de Instrução")
    religion = models.CharField(max_length=100, null=True, blank=True, verbose_name="Religião/Crença")
    sus_card_number = models.CharField(max_length=15, null=True, blank=True, verbose_name="Número do Cartão SUS")
    health_insurance = models.CharField(max_length=100, null=True, blank=True, verbose_name="Convênio/Plano de Saúde")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

class Antecedentes(models.Model):
    profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    doencas_cronicas = models.TextField(default='', blank=True, verbose_name="Doenças Crônicas")
    cirurgias = models.TextField(default='', blank=True, verbose_name="Cirurgias")
    historico_familiar = models.TextField(default='', blank=True, verbose_name="Histórico Familiar")
    habitos = models.TextField(default='', blank=True, verbose_name="Hábitos de Vida")

    def __str__(self):
        return f"Antecedentes de {self.profile.user.username}"

class DadosBiometricos(models.Model):
    profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    altura = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, verbose_name="Altura (m)")
    peso = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Peso (kg)")
    pressao_arterial = models.CharField(max_length=20, default='', blank=True, verbose_name="Pressão Arterial")
    tipo_sanguineo = models.CharField(max_length=5, default='', blank=True, verbose_name="Tipo Sanguíneo")

    def __str__(self):
        return f"Dados Biométricos de {self.profile.user.username}"

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
