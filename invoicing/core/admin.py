from .models import Invoice, InvoiceItem, Tax, Discount, InvoiceFile, Product
from django.contrib import admin
from django.contrib.auth.models import Permission
from django.contrib.auth import get_user_model
from django.urls import reverse

# Register your models here.
'''
@admin.register(get_user_model())
class InvoiceUserAdmin(admin.ModelAdmin):
  list_display = ["username", "email"]
  search_fields = ["username", "email"]
'''

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
  list_display = ["__str__", "client", "invoicer", "issued_on", "items"]
  search_fields = ["client__name_on_invoice", "issued_on", "id"]
  list_select_related = True

  def items(self, obj):
    app_label = obj.items.all()[0]._meta.app_label
    model_name = obj.items.all()[0]._meta.model_name

    url = reverse(f"admin:{app_label}_{model_name}_changelist", kwargs={"uuid": obj.uuid})
    return f"<a href=\"{url}\">items</a>"

@admin.register(InvoiceItem)
class InvoiceItemAdmin(admin.ModelAdmin):
  list_display = ["invoice_id", "invoice", "sku", "name", "description"]
  search_fields = ["sku", "name", "description"]

@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):
  list_display = ["name", "tax_type", "percentage"]
  search_fields = ["name", "tax_type", "percentage"]

@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
  list_display = ["__str__", "charge_type", "amount"]
  search_fields = ["__str__", "charge_type", "amount"]

@admin.register(InvoiceFile)
class InvoiceFileAdmin(admin.ModelAdmin):
  list_display = ["file", "invoice"]
  search_fields = ["file", "invoice"]

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
  list_display = ["name", "cost", "sku", "description", "note"]
  search_fields = ["name", "cost", "sku", "description", "note"]
