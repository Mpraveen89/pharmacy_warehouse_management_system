from django.contrib import admin
from .models import Address, Location, Medicine, Batch, StockMovement

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("name","city","state","country")
    search_fields = ("name","city","state","postal_code")

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("code","name","aisle","shelf","bin")
    search_fields = ("code","name","aisle","shelf","bin")

@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ("name","dosage_form","strength","category","upc")
    search_fields = ("name","strength","upc","category")
    list_filter = ("dosage_form","category")

@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display = ("medicine","lot_no","mfg_date","exp_date","quantity","location")
    list_filter = ("location","medicine__dosage_form")
    search_fields = ("lot_no","medicine__name")

@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ("move_type","batch","quantity","ref_no","counterparty","moved_at")
    list_filter = ("move_type","moved_at")
    search_fields = ("ref_no","batch__lot_no","batch__medicine__name")
