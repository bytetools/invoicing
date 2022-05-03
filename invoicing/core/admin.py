from .models import Invoice, InvoiceItem, Country, Region, Municipality, Address, Tax, Discount, InvoiceFile, Client, Product
from django.contrib import admin
from django.contrib.auth.models import Permission
from django.contrib.auth import get_user_model

# Register your models here.
'''
@admin.register(get_user_model())
class InvoiceUserAdmin(admin.ModelAdmin):
  list_display = ["username", "email"]
  search_fields = ["username", "email"]
'''

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
  list_display = ["__str__", "client", "invoicer", "issued_on"]
  search_fields = ["__str__", "client", "invoicer", "issued_on"]

@admin.register(InvoiceItem)
class InvoiceItemAdmin(admin.ModelAdmin):
  list_display = ["invoice_id", "invoice", "sku", "name", "description"]
  search_fields = ["invoice_id", "invoice", "sku", "name", "description"]

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

@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):
  list_display = ["name", "tax_type", "percentage"]
  search_fields = ["name", "tax_type", "percentage"]

@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
  list_display = ["__str__", "discount_type", "amount"]
  search_fields = ["__str__", "discount_type", "amount"]

@admin.register(InvoiceFile)
class InvoiceFileAdmin(admin.ModelAdmin):
  list_display = ["file", "invoice"]
  search_fields = ["file", "invoice"]

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
  list_display = ["name", "address"]
  search_fields = ["name", "address"]

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
  list_display = ["name", "cost", "sku", "description", "note"]
  search_fields = ["name", "cost", "sku", "description", "note"]
