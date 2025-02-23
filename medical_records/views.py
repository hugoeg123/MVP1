from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import MedicalRecord, Attachment

class MedicalRecordListView(LoginRequiredMixin, ListView):
    model = MedicalRecord
    template_name = 'medical_records/record_list.html'
    context_object_name = 'records'

    def get_queryset(self):
        if self.request.user.userprofile.is_doctor:
            return MedicalRecord.objects.filter(doctor=self.request.user)
        return MedicalRecord.objects.filter(patient=self.request.user)

class MedicalRecordDetailView(LoginRequiredMixin, DetailView):
    model = MedicalRecord
    template_name = 'medical_records/record_detail.html'
    context_object_name = 'record'

    def get_queryset(self):
        if self.request.user.userprofile.is_doctor:
            return MedicalRecord.objects.filter(doctor=self.request.user)
        return MedicalRecord.objects.filter(patient=self.request.user)

class MedicalRecordCreateView(LoginRequiredMixin, CreateView):
    model = MedicalRecord
    template_name = 'medical_records/record_form.html'
    fields = ['patient', 'diagnosis', 'treatment', 'prescription', 'notes']
    success_url = reverse_lazy('record-list')

    def form_valid(self, form):
        form.instance.doctor = self.request.user
        return super().form_valid(form)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if not self.request.user.userprofile.is_doctor:
            form.fields['patient'].widget.attrs['disabled'] = True
        return form

class MedicalRecordUpdateView(LoginRequiredMixin, UpdateView):
    model = MedicalRecord
    template_name = 'medical_records/record_form.html'
    fields = ['diagnosis', 'treatment', 'prescription', 'notes']
    success_url = reverse_lazy('record-list')

    def get_queryset(self):
        if self.request.user.userprofile.is_doctor:
            return MedicalRecord.objects.filter(doctor=self.request.user)
        return MedicalRecord.objects.none()
