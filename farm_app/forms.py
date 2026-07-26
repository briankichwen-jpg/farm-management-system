from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import FarmerProfile, Crop, Livestock, InventoryItem, FarmingPlan

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already registered.')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class FarmerProfileForm(forms.ModelForm):
    class Meta:
        model = FarmerProfile
        fields = ['date_of_birth', 'phone_number', 'location', 'farm_name', 'farm_size']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone number'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Location'}),
            'farm_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Farm name'}),
            'farm_size': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Farm size (hectares)', 'step': '0.01'}),
        }

class CropForm(forms.ModelForm):
    class Meta:
        model = Crop
        fields = ['crop_type', 'variety', 'planting_date', 'harvest_date', 'land_size', 
                  'labour_cost', 'fertilizer_cost', 'herbicide_cost', 'pesticide_cost', 
                  'quantity_harvested', 'selling_price', 'status', 'notes']
        widgets = {
            'crop_type': forms.Select(attrs={'class': 'form-control'}),
            'variety': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Crop variety'}),
            'planting_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'harvest_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'land_size': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Land size (hectares)'}),
            'labour_cost': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'fertilizer_cost': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'herbicide_cost': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'pesticide_cost': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'quantity_harvested': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'selling_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class LivestockForm(forms.ModelForm):
    class Meta:
        model = Livestock
        fields = ['livestock_type', 'breed', 'date_of_birth', 'number_of_animals',
                  'feed_cost', 'labour_cost', 'veterinary_cost', 'medicine_cost',
                  'vaccination_records', 'sales', 'notes']
        widgets = {
            'livestock_type': forms.Select(attrs={'class': 'form-control'}),
            'breed': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Breed'}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'number_of_animals': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'feed_cost': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'labour_cost': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'veterinary_cost': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'medicine_cost': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'vaccination_records': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'sales': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class InventoryItemForm(forms.ModelForm):
    class Meta:
        model = InventoryItem
        fields = ['item_type', 'item_name', 'quantity', 'unit', 'purchase_date',
                  'purchase_price', 'current_stock', 'notes']
        widgets = {
            'item_type': forms.Select(attrs={'class': 'form-control'}),
            'item_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Item name'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'unit': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Unit (kg, liters, etc)'}),
            'purchase_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'purchase_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'current_stock': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class FarmingPlanForm(forms.ModelForm):
    class Meta:
        model = FarmingPlan
        fields = ['month', 'activity', 'crop', 'livestock', 'description', 'status']
        widgets = {
            'month': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'activity': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Activity'}),
            'crop': forms.Select(attrs={'class': 'form-control'}),
            'livestock': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }
