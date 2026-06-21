from django.shortcuts import render, redirect
from django.views.generic import UpdateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from .models import Business, BusinessSettings

class BusinessCreateView(LoginRequiredMixin, CreateView):
    model = Business
    template_name = 'tenants/form.html'  # Assuming you have a form template
    fields = ['name', 'slug', 'description', 'phone', 'address', 'logo']
    success_url = reverse_lazy('dashboard')
    
    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.success(self.request, 'Business created successfully!')
        return super().form_valid(form)

class BusinessSettingsView(LoginRequiredMixin, UpdateView):
    model = Business
    template_name = 'tenants/settings.html'
    fields = ['name', 'description', 'phone', 'address', 'logo']
    success_url = reverse_lazy('tenants:settings')
    
    def get_object(self):
        return self.request.user.business
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['settings'] = BusinessSettings.objects.get_or_create(business=self.object)[0]
        context['working_days'] = [
            {'value': 0, 'name': 'Monday'},
            {'value': 1, 'name': 'Tuesday'},
            {'value': 2, 'name': 'Wednesday'},
            {'value': 3, 'name': 'Thursday'},
            {'value': 4, 'name': 'Friday'},
            {'value': 5, 'name': 'Saturday'},
            {'value': 6, 'name': 'Sunday'},
        ]
        return context
    
    def form_valid(self, form):
        messages.success(self.request, 'Business settings updated successfully!')
        return super().form_valid(form)

@login_required
def business_profile(request):
    return render(request, 'tenants/profile.html')

@login_required
def working_hours(request):
    return render(request, 'tenants/working_hours.html')