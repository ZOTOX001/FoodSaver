from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'role', 'restaurant_license', 'ngo_registration', 'institution_name', 'address', 'latitude', 'longitude')
        widgets = {
            'latitude': forms.HiddenInput(),
            'longitude': forms.HiddenInput(),
        }

    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get('role')
        if role == 'donor' and not cleaned_data.get('restaurant_license'):
            self.add_error('restaurant_license', 'Restaurant License is required for Donors.')
        if role == 'claimant' and not cleaned_data.get('ngo_registration'):
            self.add_error('ngo_registration', 'NGO Registration is required for Claimants.')
        return cleaned_data
