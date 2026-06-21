from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Payment

class PaymentHistoryView(LoginRequiredMixin, ListView):
    model = Payment
    template_name = 'payments/history.html'
    context_object_name = 'payments'
    
    def get_queryset(self):
        return Payment.objects.filter(booking__business=self.request.user.business)

@login_required
def download_invoice(request, payment_id):
    # Generate invoice PDF
    return HttpResponse("Invoice PDF")

def payment_webhook(request):
    # Handle payment gateway webhooks
    return HttpResponse("Webhook received")