from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Booking

class BookingListView(LoginRequiredMixin, ListView):
    model = Booking
    template_name = 'bookings/list.html'
    context_object_name = 'bookings'
    
    def get_queryset(self):
        if self.request.user.role == 'business_owner':
            return Booking.objects.filter(business__owner=self.request.user)
        elif self.request.user.role == 'staff':
            return Booking.objects.filter(staff__user=self.request.user)
        else:
            return Booking.objects.filter(customer=self.request.user)

class BookingDetailView(LoginRequiredMixin, DetailView):
    model = Booking
    template_name = 'bookings/detail.html'

class BookingCreateView(LoginRequiredMixin, CreateView):
    model = Booking
    template_name = 'bookings/form.html'
    fields = ['service', 'staff', 'booking_date', 'start_time', 'notes']
    
    def form_valid(self, form):
        form.instance.customer = self.request.user
        messages.success(self.request, 'Booking created successfully!')
        return super().form_valid(form)

def public_booking(request, business_slug):
    return render(request, 'bookings/public_booking.html')

def booking_success(request, booking_id):
    return render(request, 'bookings/success.html', {'booking_id': booking_id})

@login_required
def cancel_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    booking.status = 'cancelled'
    booking.save()
    messages.success(request, 'Booking cancelled successfully!')
    return redirect('bookings:list')

@login_required
def confirm_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    booking.status = 'confirmed'
    booking.save()
    messages.success(request, 'Booking confirmed!')
    return redirect('bookings:list')

@login_required
def start_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    booking.status = 'in_progress'
    booking.save()
    return redirect('bookings:detail', pk=pk)

@login_required
def complete_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    booking.status = 'completed'
    booking.save()
    messages.success(request, 'Booking completed!')
    return redirect('bookings:list')