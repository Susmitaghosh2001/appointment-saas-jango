from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from .models import Service

class ServiceListView(LoginRequiredMixin, ListView):
    model = Service
    template_name = 'services/list.html'
    context_object_name = 'services'
    
    def get_queryset(self):
        return Service.objects.filter(business=self.request.user.business)

class ServiceCreateView(LoginRequiredMixin, CreateView):
    model = Service
    template_name = 'services/form.html'
    fields = ['name', 'description', 'duration_minutes', 'price', 'is_active']
    success_url = reverse_lazy('services:list')
    
    def form_valid(self, form):
        if not self.request.user.business:
            form.add_error(None, 'You must create a business first before adding services.')
            messages.error(self.request, 'Please set up your business before adding services.')
            return self.form_invalid(form)
        form.instance.business = self.request.user.business
        messages.success(self.request, 'Service created successfully!')
        return super().form_valid(form)

class ServiceUpdateView(LoginRequiredMixin, UpdateView):
    model = Service
    template_name = 'services/form.html'
    fields = ['name', 'description', 'duration_minutes', 'price', 'is_active']
    success_url = reverse_lazy('services:list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Service updated successfully!')
        return super().form_valid(form)

class ServiceDeleteView(LoginRequiredMixin, DeleteView):
    model = Service
    success_url = reverse_lazy('services:list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Service deleted successfully!')
        return super().delete(request, *args, **kwargs)

@login_required
def toggle_service(request, pk):
    service = get_object_or_404(Service, pk=pk, business=request.user.business)
    service.is_active = not service.is_active
    service.save()
    status = 'activated' if service.is_active else 'deactivated'
    messages.success(request, f'Service {status} successfully!')
    return redirect('services:list')