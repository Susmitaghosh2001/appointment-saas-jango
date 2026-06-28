from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q

from apps.subscriptions.models import Subscription, Plan
from apps.services.models import ServiceType, Service
from apps.accounts.models import User as CustomUser
from .admin_forms import AdminSubscriptionForm, AdminServiceTypeForm, AdminServiceForm


def admin_required(view_func):
    """Decorator to check if user is super admin"""
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role != 'super_admin':
            messages.error(request, 'Access denied.')
            return redirect('admin_login')
        return view_func(request, *args, **kwargs)
    return wrapper


@login_required
@admin_required
def subscriptions_list(request):
    """List all subscriptions with pagination and search"""
    query = request.GET.get('q', '')
    subscriptions = Subscription.objects.select_related('business', 'plan').all()
    
    if query:
        subscriptions = subscriptions.filter(
            Q(business__name__icontains=query) |
            Q(plan__name__icontains=query) |
            Q(business__owner__email__icontains=query)
        )
    
    paginator = Paginator(subscriptions, 25)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'admin/subscriptions/list.html', {
        'page_obj': page_obj,
        'query': query,
    })


@login_required
@admin_required
def subscriptions_create(request):
    """Create a new subscription"""
    if request.method == 'POST':
        form = AdminSubscriptionForm(request.POST)
        if form.is_valid():
            subscription = form.save()
            messages.success(request, f'Subscription created successfully for {subscription.business.name}.')
            return redirect('admin:subscriptions_list')
    else:
        form = AdminSubscriptionForm()
    
    return render(request, 'admin/subscriptions/form.html', {
        'form': form,
        'title': 'Create Subscription',
        'action': 'Create',
    })


@login_required
@admin_required
def subscriptions_update(request, subscription_id):
    """Update an existing subscription"""
    subscription = get_object_or_404(Subscription, id=subscription_id)
    
    if request.method == 'POST':
        form = AdminSubscriptionForm(request.POST, instance=subscription)
        if form.is_valid():
            subscription = form.save()
            messages.success(request, f'Subscription updated successfully for {subscription.business.name}.')
            return redirect('admin:subscriptions_list')
    else:
        form = AdminSubscriptionForm(instance=subscription)
    
    return render(request, 'admin/subscriptions/form.html', {
        'form': form,
        'title': f'Edit Subscription - {subscription.business.name}',
        'action': 'Update',
    })


@login_required
@admin_required
def subscriptions_delete(request, subscription_id):
    """Delete a subscription"""
    subscription = get_object_or_404(Subscription, id=subscription_id)
    
    if request.method == 'POST':
        business_name = subscription.business.name
        subscription.delete()
        messages.success(request, f'Subscription for {business_name} deleted successfully.')
        return redirect('admin:subscriptions_list')
    
    return render(request, 'admin/subscriptions/confirm_delete.html', {
        'subscription': subscription,
    })


@login_required
@admin_required
def service_types_list(request):
    """List all service types with pagination and search"""
    query = request.GET.get('q', '')
    service_types = ServiceType.objects.all()
    
    if query:
        service_types = service_types.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )
    
    paginator = Paginator(service_types, 25)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'admin/service_types/list.html', {
        'page_obj': page_obj,
        'query': query,
    })


@login_required
@admin_required
def service_types_create(request):
    """Create a new service type"""
    if request.method == 'POST':
        form = AdminServiceTypeForm(request.POST)
        if form.is_valid():
            service_type = form.save()
            messages.success(request, f'Service type "{service_type.name}" created successfully.')
            return redirect('admin:service_types_list')
    else:
        form = AdminServiceTypeForm()
    
    return render(request, 'admin/service_types/form.html', {
        'form': form,
        'title': 'Create Service Type',
        'action': 'Create',
    })


@login_required
@admin_required
def service_types_update(request, service_type_id):
    """Update an existing service type"""
    service_type = get_object_or_404(ServiceType, id=service_type_id)
    
    if request.method == 'POST':
        form = AdminServiceTypeForm(request.POST, instance=service_type)
        if form.is_valid():
            service_type = form.save()
            messages.success(request, f'Service type "{service_type.name}" updated successfully.')
            return redirect('admin:service_types_list')
    else:
        form = AdminServiceTypeForm(instance=service_type)
    
    return render(request, 'admin/service_types/form.html', {
        'form': form,
        'title': f'Edit Service Type - {service_type.name}',
        'action': 'Update',
    })


@login_required
@admin_required
def service_types_delete(request, service_type_id):
    """Delete a service type"""
    service_type = get_object_or_404(ServiceType, id=service_type_id)
    
    if request.method == 'POST':
        name = service_type.name
        service_type.delete()
        messages.success(request, f'Service type "{name}" deleted successfully.')
        return redirect('admin:service_types_list')
    
    return render(request, 'admin/service_types/confirm_delete.html', {
        'service_type': service_type,
    })


@login_required
@admin_required
def services_list(request):
    """List all services with pagination and search"""
    query = request.GET.get('q', '')
    services = Service.objects.select_related('business', 'service_type').all()
    
    if query:
        services = services.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(business__name__icontains=query) |
            Q(service_type__name__icontains=query)
        )
    
    paginator = Paginator(services, 25)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'admin/services/list.html', {
        'page_obj': page_obj,
        'query': query,
    })


@login_required
@admin_required
def users_list(request):
    """List all users with pagination and search"""
    query = request.GET.get('q', '')
    users = CustomUser.objects.all()
    
    if query:
        users = users.filter(
            Q(email__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)
        )
    
    paginator = Paginator(users, 25)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'admin/users/list.html', {
        'page_obj': page_obj,
        'query': query,
    })
