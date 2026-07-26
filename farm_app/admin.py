from django.contrib import admin
from .models import FarmerProfile, Crop, Livestock, InventoryItem, FarmingPlan, FinancialRecord

@admin.register(FarmerProfile)
class FarmerProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'farm_name', 'location', 'created_at']
    search_fields = ['user__email', 'farm_name', 'location']
    list_filter = ['created_at']

@admin.register(Crop)
class CropAdmin(admin.ModelAdmin):
    list_display = ['farmer', 'crop_type', 'variety', 'status', 'planting_date']
    search_fields = ['farmer__user__email', 'variety', 'crop_type']
    list_filter = ['crop_type', 'status', 'planting_date']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Livestock)
class LivestockAdmin(admin.ModelAdmin):
    list_display = ['farmer', 'livestock_type', 'breed', 'number_of_animals']
    search_fields = ['farmer__user__email', 'breed', 'livestock_type']
    list_filter = ['livestock_type', 'created_at']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ['farmer', 'item_type', 'item_name', 'current_stock', 'unit']
    search_fields = ['farmer__user__email', 'item_name', 'item_type']
    list_filter = ['item_type', 'purchase_date']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(FarmingPlan)
class FarmingPlanAdmin(admin.ModelAdmin):
    list_display = ['farmer', 'activity', 'status', 'month']
    search_fields = ['farmer__user__email', 'activity']
    list_filter = ['status', 'month']

@admin.register(FinancialRecord)
class FinancialRecordAdmin(admin.ModelAdmin):
    list_display = ['farmer', 'date', 'income', 'expenses']
    search_fields = ['farmer__user__email']
    list_filter = ['date']
    readonly_fields = ['created_at']
