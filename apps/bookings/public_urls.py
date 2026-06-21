from django.urls import path
from . import views

app_name = 'public_bookings'

urlpatterns = [
    path('', views.public_booking, name='book'),
    path('success/<uuid:booking_id>/', views.booking_success, name='success'),
]