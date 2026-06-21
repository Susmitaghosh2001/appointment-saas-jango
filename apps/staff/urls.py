from django.urls import path
from . import views

app_name = 'staff'

urlpatterns = [
    path('', views.StaffListView.as_view(), name='list'),
    path('create/', views.StaffCreateView.as_view(), name='create'),
    path('<int:pk>/edit/', views.StaffUpdateView.as_view(), name='edit'),
    path('<int:pk>/availability/', views.StaffAvailabilityView.as_view(), name='availability'),
    path('<int:pk>/toggle/', views.toggle_staff, name='toggle'),
]