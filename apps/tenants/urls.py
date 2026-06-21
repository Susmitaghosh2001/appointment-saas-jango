from django.urls import path
from . import views

app_name = 'tenants'

urlpatterns = [
    path('create/', views.BusinessCreateView.as_view(), name='create'),
    path('', views.BusinessSettingsView.as_view(), name='settings'),
    path('profile/', views.business_profile, name='profile'),
    path('working-hours/', views.working_hours, name='working_hours'),
]