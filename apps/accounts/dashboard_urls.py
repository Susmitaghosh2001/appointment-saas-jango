from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

app_name = 'dashboard'

urlpatterns = [
    # Main dashboard - redirects to role-specific dashboard
    path('', login_required(views.dashboard), name='home'),
    
    # Admin Dashboard
    path('admin/', login_required(views.super_admin_dashboard), name='admin'),
    path('admin/<uuid:business_id>/change-plan/', login_required(views.super_admin_change_plan), name='admin_change_plan'),
    path('admin/<uuid:business_id>/toggle-business/', login_required(views.super_admin_toggle_business), name='admin_toggle_business'),
    
    # Business Owner Dashboard
    path('business/', login_required(views.business_dashboard), name='business'),
    
    # Staff Dashboard
    path('staff/', login_required(views.staff_dashboard), name='staff'),
    
#     # Customer Dashboard
#     path('customer/', login_required(views.CustomerDashboardView.as_view()), name='customer'),
    
#     # Analytics Dashboard (for business owners)
#     path('analytics/', login_required(views.AnalyticsDashboardView.as_view()), name='analytics'),
    
#     # Recent Activity
#     path('recent-activity/', login_required(views.recent_activity), name='recent_activity'),
 ]