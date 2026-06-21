from django import forms
from .models import Service

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'description', 'duration_minutes', 'price', 'is_active']

        widgets = {
    'name': forms.TextInput(attrs={
        'class': 'w-full px-4 py-2.5 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:outline-none'
    }),
    'description': forms.Textarea(attrs={
        'class': 'w-full px-4 py-2.5 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:outline-none'
    }),
    'duration_minutes': forms.NumberInput(attrs={
        'class': 'w-full px-4 py-2.5 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-500'
    }),
    'price': forms.NumberInput(attrs={
        'class': 'w-full px-4 py-2.5 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-500'
    }),
    'is_active': forms.CheckboxInput(attrs={
        'class': 'h-5 w-5 text-blue-600'
    })
}

        error_messages = {
            'name': {
                'required': 'Service name is required.',
                'max_length': 'Service name cannot exceed 255 characters.'
            },
            'duration_minutes': {
                'required': 'Duration is required.',
                'invalid': 'Enter a valid number for duration.'
            },
            'price': {
                'required': 'Price is required.',
                'invalid': 'Enter a valid price.'
            }
        }

    # 🔹 Custom validation methods

    def clean_name(self):
        name = self.cleaned_data.get('name')

        if not name:
            raise forms.ValidationError("Please enter the service name.")

        if len(name.strip()) < 3:
            raise forms.ValidationError("Service name must be at least 3 characters long.")

        return name.strip()

    def clean_duration_minutes(self):
        duration = self.cleaned_data.get('duration_minutes')

        if duration is None:
            raise forms.ValidationError("Please enter duration.")

        if duration < 5:
            raise forms.ValidationError("Duration must be at least 5 minutes.")

        if duration % 5 != 0:
            raise forms.ValidationError("Duration should be in multiples of 5 (e.g., 5, 10, 15).")

        return duration

    def clean_price(self):
        price = self.cleaned_data.get('price')

        if price is None:
            raise forms.ValidationError("Please enter price.")

        if price < 0:
            raise forms.ValidationError("Price cannot be negative.")

        return price

    # 🔹 Cross-field validation (optional but powerful)
    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        business = self.instance.business if self.instance else None

        # Prevent duplicate service name per business
        if name and business:
            if Service.objects.filter(
                business=business,
                name__iexact=name
            ).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError(
                    "A service with this name already exists for this business."
                )

        return cleaned_data