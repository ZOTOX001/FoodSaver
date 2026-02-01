from django import forms
from .models import Listing

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ('food_type', 'quantity_kg', 'servings', 'description', 'expiry_time', 'pickup_instructions', 'image')
        widgets = {
            'expiry_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'rows': 3}),
            'pickup_instructions': forms.Textarea(attrs={'rows': 2}),
        }
