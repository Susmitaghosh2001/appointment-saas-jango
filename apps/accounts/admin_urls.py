from django.urls import path
from django.views.generic import RedirectView
from . import admin_views

app_name = 'admin'

urlpatterns = [
    # Subscriptions
    path('subscriptions/', admin_views.subscriptions_list, name='subscriptions_list'),
    path('subscriptions/create/', admin_views.subscriptions_create, name='subscriptions_create'),
    path('subscriptions/<uuid:subscription_id>/edit/', admin_views.subscriptions_update, name='subscriptions_update'),
    path('subscriptions/<uuid:subscription_id>/delete/', admin_views.subscriptions_delete, name='subscriptions_delete'),
    
    # Service Types
    path('service-types/', admin_views.service_types_list, name='service_types_list'),
    path('service-types/create/', admin_views.service_types_create, name='service_types_create'),
    path('service-types/<int:service_type_id>/edit/', admin_views.service_types_update, name='service_types_update'),
    path('service-types/<int:service_type_id>/delete/', admin_views.service_types_delete, name='service_types_delete'),
    
    # Services
    path('services/', admin_views.services_list, name='services_list'),
    
    # Users
    path('users/', admin_views.users_list, name='users_list'),
    
    # Django Admin
    path('site-admin/', RedirectView.as_view(url='/admin/', permanent=False), name='site_admin'),
]
