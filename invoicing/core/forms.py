from datetime import date
from .models import Invoice, InvoiceItem, Client, Address, Region, Country, Municipality, Tax, Product
from django import forms
from django.forms import widgets

class InvoiceForm(forms.ModelForm):
  class Meta:
    model = Invoice
    exclude = []
    widgets = {
      "issued_on": widgets.SelectDateWidget(),
      "due_date": widgets.SelectDateWidget()
    }

class InvoiceItemForm(forms.ModelForm):
  class Meta:
    model = InvoiceItem
    exclude = []

class ClientForm(forms.ModelForm):
  class Meta:
    model = Client
    exclude = []

class AddressForm(forms.ModelForm):
  class Meta:
    model = Address
    exclude = []
class CountryForm(forms.ModelForm):
  class Meta:
    model = Country
    exclude = []
class RegionForm(forms.ModelForm):
  class Meta:
    model = Region
    exclude = []
class MunicipalityForm(forms.ModelForm):
  class Meta:
    model = Municipality
    exclude = []

class TaxForm(forms.ModelForm):
  class Meta:
    model = Tax
    exclude = []

class ProductForm(forms.ModelForm):
  class Meta:
    model = Product
    exclude = []
