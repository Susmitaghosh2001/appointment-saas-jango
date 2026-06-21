from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from .models import Staff

class StaffListView(LoginRequiredMixin, ListView):
    model = Staff
    template_name = 'staff/list.html'
    context_object_name = 'staff_members'
    
    def get_queryset(self):
        return Staff.objects.filter(business=self.request.user.business)

class StaffCreateView(LoginRequiredMixin, CreateView):
    model = Staff
    template_name = 'staff/form.html'
    fields = ['user', 'phone', 'is_active']
    success_url = reverse_lazy('staff:list')
    
    def form_valid(self, form):
        if not self.request.user.business:
            form.add_error(None, 'You must create a business first before adding staff.')
            return self.form_invalid(form)
        form.instance.business = self.request.user.business
        messages.success(self.request, 'Staff member added successfully!')
        return super().form_valid(form)

class StaffUpdateView(LoginRequiredMixin, UpdateView):
    model = Staff
    template_name = 'staff/form.html'
    fields = ['phone', 'is_active', 'services']
    success_url = reverse_lazy('staff:list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Staff information updated!')
        return super().form_valid(form)

class StaffAvailabilityView(LoginRequiredMixin, UpdateView):
    model = Staff
    template_name = 'staff/availability.html'
    fields = []
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['days'] = [
            {'value': 0, 'name': 'Monday'},
            {'value': 1, 'name': 'Tuesday'},
            {'value': 2, 'name': 'Wednesday'},
            {'value': 3, 'name': 'Thursday'},
            {'value': 4, 'name': 'Friday'},
            {'value': 5, 'name': 'Saturday'},
            {'value': 6, 'name': 'Sunday'},
        ]
        return context

@login_required
def toggle_staff(request, pk):
    staff = get_object_or_404(Staff, pk=pk, business=request.user.business)
    staff.is_active = not staff.is_active
    staff.save()
    status = 'activated' if staff.is_active else 'deactivated'
    messages.success(request, f'Staff member {status}!')
    return redirect('staff:list')