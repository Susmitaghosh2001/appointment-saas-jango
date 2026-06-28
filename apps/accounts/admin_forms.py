from django import forms
from apps.subscriptions.models import Subscription, Plan
from apps.services.models import ServiceType, Service


class AdminSubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ['business', 'plan', 'start_date', 'end_date', 'is_active', 'payment_status']
        widgets = {
            'business': forms.Select(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500'}),
            'plan': forms.Select(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500'}),
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'w-4 h-4 border border-gray-300 rounded focus:ring-blue-500'}),
            'payment_status': forms.Select(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500'}),
        }


class AdminServiceTypeForm(forms.ModelForm):
    class Meta:
        model = ServiceType
        fields = ['name', 'description', 'icon', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500', 'placeholder': 'e.g., Haircut, Massage, Dental'}),
            'description': forms.Textarea(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500', 'rows': 4, 'placeholder': 'Service type description'}),
            'icon': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500', 'placeholder': 'e.g., fa-scissors, fa-spa, fa-tooth'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'w-4 h-4 border border-gray-300 rounded focus:ring-blue-500'}),
        }


class AdminServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['business', 'service_type', 'name', 'description', 'duration_minutes', 'price', 'is_active']
        widgets = {
            'business': forms.Select(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500'}),
            'service_type': forms.Select(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500'}),
            'name': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500', 'placeholder': 'Service name'}),
            'description': forms.Textarea(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500', 'rows': 4}),
            'duration_minutes': forms.NumberInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500', 'min': 5}),
            'price': forms.NumberInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500', 'min': 0, 'step': 0.01}),
            'is_active': forms.CheckboxInput(attrs={'class': 'w-4 h-4 border border-gray-300 rounded focus:ring-blue-500'}),
        }
