from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from farm_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='farm_app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
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
    path('plans/', views.farming_plan_list, name='farming_plan_list'),
    path('plans/create/', views.farming_plan_create, name='farming_plan_create'),
    path('plans/<int:pk>/edit/', views.farming_plan_edit, name='farming_plan_edit'),
    
    # Analytics
    path('analytics/', views.analytics, name='analytics'),
]
