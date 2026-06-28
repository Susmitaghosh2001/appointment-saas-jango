from datetime import timedelta

from functools import wraps
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.utils import timezone

from .models import UserProfile, User as CustomUser
from apps.tenants.models import Business
from apps.subscriptions.models import Plan, Subscription


def register(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')
        role = request.POST.get('role', 'customer')
        business_name = request.POST.get('business_name', '').strip()
        
        # Validation
        if not all([full_name, email, password1, password2]):
            messages.error(request, 'All fields are required!')
            return render(request, 'accounts/register.html')
        
        if password1 != password2:
            messages.error(request, 'Passwords do not match!')
            return render(request, 'accounts/register.html')
        
        if len(password1) < 6:
            messages.error(request, 'Password must be at least 6 characters!')
            return render(request, 'accounts/register.html')
        
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered!')
            return render(request, 'accounts/register.html')
        
        # Create user with transaction to ensure both User and UserProfile are created
        try:
            with transaction.atomic():
                # Use email as username since email is the USERNAME_FIELD
                user = CustomUser.objects.create_user(
                    username=email,
                    email=email,
                    password=password1,
                    role=role
                )
                
                # Create associated UserProfile
                profile = UserProfile.objects.create(user=user)
                
                # Update user with the full name from the form
                user.first_name = full_name.split()[0] if full_name else ''
                user.last_name = ' '.join(full_name.split()[1:]) if len(full_name.split()) > 1 else ''
                user.phone = phone
                user.save()
                
                messages.success(request, 'Account created successfully! Please log in.')
                return redirect('accounts:login')
        except Exception as e:
            messages.error(request, f'Error creating account: {str(e)}')
            return render(request, 'accounts/register.html')
    
    return render(request, 'accounts/register.html')

def admin_login(request):
    if request.user.is_authenticated and request.user.role == 'super_admin':
        return redirect('admin_dashboard')

    if request.method == 'POST':
        email = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=email, password=password)

        if user is not None:
            if user.role == 'super_admin':
                login(request, user)
                return redirect('admin_dashboard')
            messages.error(request, 'This account does not have admin access.')
        else:
            messages.error(request, 'Invalid email or password.')

    return render(request, 'accounts/admin_login.html')


def super_admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role != 'super_admin':
            return redirect('admin_login')
        return view_func(request, *args, **kwargs)
    return wrapper

@login_required
def profile(request):
    return render(request, 'accounts/profile.html', {'user': request.user})

@login_required
def dashboard(request):
    if request.user.role == 'super_admin':
        return redirect('admin_dashboard')
    if request.user.role == 'business_owner':
        return redirect('dashboard:business')
    elif request.user.role == 'staff':
        return redirect('dashboard:staff')
    else:
        return render(request, 'dashboard/customer.html')

@login_required
def business_dashboard(request):
    return render(request, 'dashboard/business_owner.html')

@login_required
def staff_dashboard(request):
    return render(request, 'dashboard/staff.html', {'user': request.user})

@super_admin_required
def super_admin_dashboard(request):
    businesses = Business.objects.select_related('owner').all()
    active_subscriptions = Subscription.objects.filter(is_active=True).count()
    plans = Plan.objects.filter(is_active=True).order_by('price')

    customer_data = []
    for business in businesses:
        subscription = business.subscriptions.filter(is_active=True).select_related('plan').first()
        active_staff = business.staff_members.filter(is_active=True).count()
        customer_data.append({
            'business': business,
            'subscription': subscription,
            'staff_count': active_staff,
        })

    return render(request, 'dashboard/super_admin.html', {
        'customer_data': customer_data,
        'plans': plans,
        'business_count': businesses.count(),
        'active_subscriptions': active_subscriptions,
    })

@super_admin_required
def admin_dashboard(request):
    return super_admin_dashboard(request)

@super_admin_required
def super_admin_change_plan(request, business_id):

    business = get_object_or_404(Business, id=business_id)
    if request.method == 'POST':
        plan_id = request.POST.get('plan_id')
        plan = get_object_or_404(Plan, id=plan_id)
        subscription = Subscription.objects.filter(business=business, is_active=True).first()

        if subscription:
            subscription.plan = plan
            subscription.save()
            messages.success(request, f"{business.name} subscription updated to {plan.name}.")
        else:
            start_date = timezone.now()
            end_date = start_date + timedelta(days=plan.duration_days)
            Subscription.objects.create(
                business=business,
                plan=plan,
                start_date=start_date,
                end_date=end_date,
                is_active=True,
                payment_status='paid'
            )
            messages.success(request, f"{business.name} now has the {plan.name} subscription.")

    return redirect('dashboard:super_admin')

@super_admin_required
def super_admin_toggle_business(request, business_id):
    business = get_object_or_404(Business, id=business_id)
    business.is_active = not business.is_active
    business.save()
    status = 'activated' if business.is_active else 'deactivated'
    messages.success(request, f"{business.name} has been {status}.")
    return redirect('dashboard:super_admin')