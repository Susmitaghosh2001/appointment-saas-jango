from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('', views.BookingListView.as_view(), name='list'),
    path('create/', views.BookingCreateView.as_view(), name='create'),
    path('<uuid:pk>/', views.BookingDetailView.as_view(), name='detail'),
    path('<uuid:pk>/cancel/', views.cancel_booking, name='cancel'),
    path('<uuid:pk>/confirm/', views.confirm_booking, name='confirm'),
    path('<uuid:pk>/start/', views.start_booking, name='start'),
    path('<uuid:pk>/complete/', views.complete_booking, name='complete'),
]