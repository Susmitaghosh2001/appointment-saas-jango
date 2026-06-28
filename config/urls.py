"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

from apps.accounts.views import admin_login, admin_dashboard

urlpatterns = [
    path('admin/login/', admin_login, name='admin_login'),
    path('admin/dashboard/', admin_dashboard, name='admin_dashboard'),
    path('admin/panel/', include('apps.accounts.admin_urls')),
    path('admin/', admin.site.urls),
    
    # Home
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    
    # Authentication
    path('accounts/', include('apps.accounts.urls')),
    
    # Dashboard
    path('dashboard/', include('apps.accounts.dashboard_urls')),
    
    # Modules
    path('bookings/', include('apps.bookings.urls')),
    path('services/', include('apps.services.urls')),
    path('staff/', include('apps.staff.urls')),
    path('subscriptions/', include('apps.subscriptions.urls')),
    path('tenants/', include('apps.tenants.urls')),
    path('settings/', include('apps.tenants.urls')),
    path('payments/', include('apps.payments.urls')),
    
    # Public booking URL with slug
    path('b/<slug:business_slug>/', include('apps.bookings.public_urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)