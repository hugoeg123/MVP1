from dal_select2.views import Select2QuerySetView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import MedicamentoAnvisa, UserMedication

@api_view(['GET'])
def medication_autocomplete(request):
    search_term = request.GET.get('q', '').strip()
    
    if len(search_term) < 2:
        return Response({'results': []})
    
    results = MedicamentoAnvisa.objects.filter(
        Q(nome_produto__icontains=search_term) | 
        Q(classe_terapeutica__icontains=search_term) |
        Q(principio_ativo__icontains=search_term)
    )[:10]

    suggestions = [{
        'id': med.id,
        'text': med.nome_produto,
        'classe_terapeutica': med.classe_terapeutica,
        'principio_ativo': med.principio_ativo
    } for med in results]

    return Response({'results': suggestions})

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
