from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Q
from django.utils import timezone
from django.http import JsonResponse
from datetime import datetime, timedelta
import json

from .models import FarmerProfile, Crop, Livestock, InventoryItem, FarmingPlan, FinancialRecord
from .forms import (UserRegistrationForm, FarmerProfileForm, CropForm, LivestockForm,
                    InventoryItemForm, FarmingPlanForm)

def home(request):
    return render(request, 'farm_app/home.html')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            farmer_profile = FarmerProfile.objects.create(user=user)
            messages.success(request, 'Account created successfully! Please log in.')
            return redirect('login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = UserRegistrationForm()
    return render(request, 'farm_app/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid email or password')
    return render(request, 'farm_app/login.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')

@login_required(login_url='login')
def dashboard(request):
    try:
        farmer = FarmerProfile.objects.get(user=request.user)
    except FarmerProfile.DoesNotExist:
        farmer = FarmerProfile.objects.create(user=request.user)

    crops = Crop.objects.filter(farmer=farmer)
    livestock = Livestock.objects.filter(farmer=farmer)
    inventory = InventoryItem.objects.filter(farmer=farmer)

    total_crops = crops.count()
    total_livestock = livestock.aggregate(Sum('number_of_animals'))['number_of_animals__sum'] or 0

    total_income = sum([crop.total_income() for crop in crops]) + sum([animal.sales for animal in livestock])
    total_expenses = sum([crop.total_expenses() for crop in crops]) + sum([animal.total_expenses() for animal in livestock])
    total_profit = total_income - total_expenses

    context = {
        'farmer': farmer,
        'current_date': timezone.now(),
        'total_crops': total_crops,
        'total_livestock': total_livestock,
        'total_income': total_income,
        'total_expenses': total_expenses,
        'total_profit': total_profit,
    }
    return render(request, 'farm_app/dashboard.html', context)

@login_required(login_url='login')
def crop_list(request):
    farmer = get_object_or_404(FarmerProfile, user=request.user)
    crops = Crop.objects.filter(farmer=farmer).order_by('-created_at')
    return render(request, 'farm_app/crop_list.html', {'crops': crops, 'farmer': farmer})

@login_required(login_url='login')
def crop_create(request):
    farmer = get_object_or_404(FarmerProfile, user=request.user)
    if request.method == 'POST':
        form = CropForm(request.POST)
        if form.is_valid():
            crop = form.save(commit=False)
            crop.farmer = farmer
            crop.save()
            messages.success(request, 'Crop added successfully!')
            return redirect('crop_list')
    else:
        form = CropForm()
    return render(request, 'farm_app/crop_form.html', {'form': form, 'action': 'Add'})

@login_required(login_url='login')
def crop_edit(request, pk):
    crop = get_object_or_404(Crop, pk=pk, farmer__user=request.user)
    if request.method == 'POST':
        form = CropForm(request.POST, instance=crop)
        if form.is_valid():
            form.save()
            messages.success(request, 'Crop updated successfully!')
            return redirect('crop_list')
    else:
        form = CropForm(instance=crop)
    return render(request, 'farm_app/crop_form.html', {'form': form, 'action': 'Edit', 'crop': crop})

@login_required(login_url='login')
def crop_detail(request, pk):
    crop = get_object_or_404(Crop, pk=pk, farmer__user=request.user)
    return render(request, 'farm_app/crop_detail.html', {'crop': crop})

@login_required(login_url='login')
def crop_delete(request, pk):
    crop = get_object_or_404(Crop, pk=pk, farmer__user=request.user)
    if request.method == 'POST':
        crop.delete()
        messages.success(request, 'Crop deleted successfully!')
        return redirect('crop_list')
    return render(request, 'farm_app/crop_confirm_delete.html', {'crop': crop})

@login_required(login_url='login')
def livestock_list(request):
    farmer = get_object_or_404(FarmerProfile, user=request.user)
    livestock = Livestock.objects.filter(farmer=farmer).order_by('-created_at')
    return render(request, 'farm_app/livestock_list.html', {'livestock': livestock, 'farmer': farmer})

@login_required(login_url='login')
def livestock_create(request):
    farmer = get_object_or_404(FarmerProfile, user=request.user)
    if request.method == 'POST':
        form = LivestockForm(request.POST)
        if form.is_valid():
            animal = form.save(commit=False)
            animal.farmer = farmer
            animal.save()
            messages.success(request, 'Livestock added successfully!')
            return redirect('livestock_list')
    else:
        form = LivestockForm()
    return render(request, 'farm_app/livestock_form.html', {'form': form, 'action': 'Add'})

@login_required(login_url='login')
def livestock_edit(request, pk):
    animal = get_object_or_404(Livestock, pk=pk, farmer__user=request.user)
    if request.method == 'POST':
        form = LivestockForm(request.POST, instance=animal)
        if form.is_valid():
            form.save()
            messages.success(request, 'Livestock updated successfully!')
            return redirect('livestock_list')
    else:
        form = LivestockForm(instance=animal)
    return render(request, 'farm_app/livestock_form.html', {'form': form, 'action': 'Edit', 'animal': animal})

@login_required(login_url='login')
def livestock_detail(request, pk):
    animal = get_object_or_404(Livestock, pk=pk, farmer__user=request.user)
    return render(request, 'farm_app/livestock_detail.html', {'animal': animal})

@login_required(login_url='login')
def livestock_delete(request, pk):
    animal = get_object_or_404(Livestock, pk=pk, farmer__user=request.user)
    if request.method == 'POST':
        animal.delete()
        messages.success(request, 'Livestock deleted successfully!')
        return redirect('livestock_list')
    return render(request, 'farm_app/livestock_confirm_delete.html', {'animal': animal})

@login_required(login_url='login')
def inventory_list(request):
    farmer = get_object_or_404(FarmerProfile, user=request.user)
    inventory = InventoryItem.objects.filter(farmer=farmer).order_by('-created_at')
    return render(request, 'farm_app/inventory_list.html', {'inventory': inventory, 'farmer': farmer})

@login_required(login_url='login')
def inventory_create(request):
    farmer = get_object_or_404(FarmerProfile, user=request.user)
    if request.method == 'POST':
        form = InventoryItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.farmer = farmer
            item.save()
            messages.success(request, 'Inventory item added successfully!')
            return redirect('inventory_list')
    else:
        form = InventoryItemForm()
    return render(request, 'farm_app/inventory_form.html', {'form': form, 'action': 'Add'})

@login_required(login_url='login')
def inventory_edit(request, pk):
    item = get_object_or_404(InventoryItem, pk=pk, farmer__user=request.user)
    if request.method == 'POST':
        form = InventoryItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Inventory item updated successfully!')
            return redirect('inventory_list')
    else:
        form = InventoryItemForm(instance=item)
    return render(request, 'farm_app/inventory_form.html', {'form': form, 'action': 'Edit', 'item': item})

@login_required(login_url='login')
def inventory_delete(request, pk):
    item = get_object_or_404(InventoryItem, pk=pk, farmer__user=request.user)
    if request.method == 'POST':
        item.delete()
        messages.success(request, 'Inventory item deleted successfully!')
        return redirect('inventory_list')
    return render(request, 'farm_app/inventory_confirm_delete.html', {'item': item})

@login_required(login_url='login')
def farming_plan_list(request):
    farmer = get_object_or_404(FarmerProfile, user=request.user)
    plans = FarmingPlan.objects.filter(farmer=farmer).order_by('month')
    return render(request, 'farm_app/farming_plan_list.html', {'plans': plans, 'farmer': farmer})

@login_required(login_url='login')
def farming_plan_create(request):
    farmer = get_object_or_404(FarmerProfile, user=request.user)
    if request.method == 'POST':
        form = FarmingPlanForm(request.POST)
        if form.is_valid():
            plan = form.save(commit=False)
            plan.farmer = farmer
            plan.save()
            messages.success(request, 'Farming plan added successfully!')
            return redirect('farming_plan_list')
    else:
        form = FarmingPlanForm()
        form.fields['crop'].queryset = Crop.objects.filter(farmer=farmer)
        form.fields['livestock'].queryset = Livestock.objects.filter(farmer=farmer)
    return render(request, 'farm_app/farming_plan_form.html', {'form': form, 'action': 'Add'})

@login_required(login_url='login')
def analytics(request):
    farmer = get_object_or_404(FarmerProfile, user=request.user)
    crops = Crop.objects.filter(farmer=farmer)
    livestock = Livestock.objects.filter(farmer=farmer)

    crop_data = [
        {
            'name': crop.variety,
            'income': float(crop.total_income()),
            'expenses': float(crop.total_expenses()),
            'profit': float(crop.profit()),
        }
        for crop in crops
    ]

    livestock_data = [
        {
            'name': animal.breed,
            'income': float(animal.sales),
            'expenses': float(animal.total_expenses()),
            'profit': float(animal.profit()),
        }
        for animal in livestock
    ]

    total_income = sum([item['income'] for item in crop_data + livestock_data])
    total_expenses = sum([item['expenses'] for item in crop_data + livestock_data])
    total_profit = total_income - total_expenses

    context = {
        'farmer': farmer,
        'crop_data': json.dumps(crop_data),
        'livestock_data': json.dumps(livestock_data),
        'total_income': total_income,
        'total_expenses': total_expenses,
        'total_profit': total_profit,
        'crops': crops,
        'livestock': livestock,
    }
    return render(request, 'farm_app/analytics.html', context)

@login_required(login_url='login')
def profile(request):
    farmer = get_object_or_404(FarmerProfile, user=request.user)
    if request.method == 'POST':
        form = FarmerProfileForm(request.POST, instance=farmer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('dashboard')
    else:
        form = FarmerProfileForm(instance=farmer)
    return render(request, 'farm_app/profile.html', {'form': form, 'farmer': farmer})
