from dal_select2.views import Select2QuerySetView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import MedicamentoAnvisa, UserMedication

class MedicamentoAutocomplete(Select2QuerySetView):
    def get_queryset(self):
        qs = MedicamentoAnvisa.objects.all()
        if self.q:
            qs = qs.filter(nome_produto__icontains=self.q) | \
                 qs.filter(classe_terapeutica__icontains=self.q) | \
                 qs.filter(principio_ativo__icontains=self.q)
        return qs

@login_required
def manage_medications(request):
    if request.method == 'POST':
        medication_id = request.POST.get('medication')
        is_allergy = request.POST.get('is_allergy') == 'true'
        notes = request.POST.get('notes', '')
        
        if medication_id:
            medication = MedicamentoAnvisa.objects.get(id=medication_id)
            UserMedication.objects.update_or_create(
                user=request.user,
                medication=medication,
                is_allergy=is_allergy,
                defaults={'notes': notes}
            )
            
        return redirect('manage_medications')
    
    medications = UserMedication.objects.filter(user=request.user, is_allergy=False)
    allergies = UserMedication.objects.filter(user=request.user, is_allergy=True)
    
    return render(request, 'medical_records/manage_medications.html', {
        'medications': medications,
        'allergies': allergies
    })

@login_required
def delete_medication(request, medication_id):
    medication = get_object_or_404(UserMedication, id=medication_id, user=request.user)
    medication.delete()
    return redirect('manage_medications')
