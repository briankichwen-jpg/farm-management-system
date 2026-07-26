from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    
    # Crop URLs
    path('crops/', views.crop_list, name='crop_list'),
    path('crops/create/', views.crop_create, name='crop_create'),
    path('crops/<int:pk>/', views.crop_detail, name='crop_detail'),
    path('crops/<int:pk>/edit/', views.crop_edit, name='crop_edit'),
    path('crops/<int:pk>/delete/', views.crop_delete, name='crop_delete'),
    
    # Livestock URLs
    path('livestock/', views.livestock_list, name='livestock_list'),
    path('livestock/create/', views.livestock_create, name='livestock_create'),
    path('livestock/<int:pk>/', views.livestock_detail, name='livestock_detail'),
    path('livestock/<int:pk>/edit/', views.livestock_edit, name='livestock_edit'),
    path('livestock/<int:pk>/delete/', views.livestock_delete, name='livestock_delete'),
    
    # Inventory URLs
    path('inventory/', views.inventory_list, name='inventory_list'),
    path('inventory/create/', views.inventory_create, name='inventory_create'),
    path('inventory/<int:pk>/edit/', views.inventory_edit, name='inventory_edit'),
    path('inventory/<int:pk>/delete/', views.inventory_delete, name='inventory_delete'),
    
    # Farming Plan URLs
    path('farming-plans/', views.farming_plan_list, name='farming_plan_list'),
    path('farming-plans/create/', views.farming_plan_create, name='farming_plan_create'),
    
    # Analytics
    path('analytics/', views.analytics, name='analytics'),
]
