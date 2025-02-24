from django.db import models
from django.conf import settings

class MedicamentoAnvisa(models.Model):
    nome_produto = models.CharField(max_length=200)
    principio_ativo = models.TextField()
    classe_terapeutica = models.CharField(max_length=200)
    
    def __str__(self):
        return f"{self.nome_produto} ({self.classe_terapeutica})"

class UserMedication(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='medications')
    medication = models.ForeignKey(MedicamentoAnvisa, on_delete=models.CASCADE)
    is_allergy = models.BooleanField(default=False)
    notes = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'medication', 'is_allergy']

    def __str__(self):
        return f"{self.user.username} - {self.medication.nome_produto} ({'Allergy' if self.is_allergy else 'Medication'})"

class MedicalRecord(models.Model):
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='medical_records')
    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='doctor_records')
    diagnosis = models.TextField()
    treatment = models.TextField()
    prescription = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Medical Record for {self.patient.username} - {self.created_at.date()}'

class Attachment(models.Model):
    medical_record = models.ForeignKey(MedicalRecord, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='medical_records/')
    description = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Attachment for {self.medical_record} - {self.description}'
