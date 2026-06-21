from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('webhook/', views.payment_webhook, name='webhook'),
    path('history/', views.PaymentHistoryView.as_view(), name='history'),
    path('invoice/<int:payment_id>/', views.download_invoice, name='invoice'),
]