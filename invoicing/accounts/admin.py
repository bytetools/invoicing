# Register your models here.
from .models import Country, Region, Municipality, Address
from django.contrib import admin
from django.contrib.auth.models import Permission
from django.contrib.auth import get_user_model

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
  list_display = ["name", "short_name"]
  search_fields = ["name", "short_name"]

@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
  list_display = ["name", "short_name", "country"]
  search_fields = ["name", "short_name", "country"]

@admin.register(Municipality)
class MunicipalityAdmin(admin.ModelAdmin):
  list_display = ["name", "region"]
  search_fields = ["name", "region"]

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
  list_display = ["street", "number", "apt_type", "apt", "municipality"]
  search_fields = ["street", "number", "apt_type", "apt", "municipality"]

@admin.register(get_user_model())
class InvoiceAccountAdmin(admin.ModelAdmin):
  list_display = ["username", "email"]
  search_fields = ["username", "email"]
