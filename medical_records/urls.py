from django.urls import path
from . import views

urlpatterns = [
    path('medicamento-autocomplete/', views.medication_autocomplete, name='medicamento-autocomplete'),
    path('manage/', views.manage_medications, name='manage_medications'),
    path('delete/<int:medication_id>/', views.delete_medication, name='delete_medication'),
]