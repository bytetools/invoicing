from datetime import date
from invoices.models import Invoice, InvoiceItem, Tax, Product
from accounts.models import Country, Region, Municipality, Address
from django import forms
from django.conf import settings
from django.forms import widgets

class InvoiceItemForm(forms.ModelForm):
  class Meta:
    model = InvoiceItem
    exclude = []
    widgets = {
      "uuid": widgets.HiddenInput(),
    }

class TaxForm(forms.ModelForm):
  class Meta:
    model = Tax
    exclude = []
    widgets = {
      "uuid": widgets.HiddenInput(),
    }

class InvoiceForm(forms.ModelForm):
  class Meta:
    model = Invoice
    exclude = []
    widgets = {
      "issued_on": widgets.SelectDateWidget(),
      "due_date": widgets.SelectDateWidget(),
      "uuid": widgets.HiddenInput(),
    }

class ProductForm(forms.ModelForm):
  class Meta:
    model = Product
    exclude = []
    widgets = {
      "uuid": forms.HiddenInput()
    }

class DeleteForm(forms.Form):
  uuid = forms.CharField(widget=widgets.HiddenInput())

class CopyForm(forms.Form):
  uuid = forms.CharField(widget=widgets.HiddenInput())

class AddressForm(forms.ModelForm):
  class Meta:
    model = Address
    exclude = []
    widgets = {
      "uuid": widgets.HiddenInput(),
    }

class CountryForm(forms.ModelForm):
  class Meta:
    model = Country
    exclude = []
    widgets = {
      "uuid": widgets.HiddenInput(),
    }

class RegionForm(forms.ModelForm):
  class Meta:
    model = Region
    exclude = []
    widgets = {
      "uuid": widgets.HiddenInput(),
    }

class MunicipalityForm(forms.ModelForm):
  class Meta:
    model = Municipality
    exclude = []
    widgets = {
      "uuid": widgets.HiddenInput(),
    }

class PaymentForm(forms.Form):
  MONTH_CHOICES = [
    ("01", "01"),
    ("02", "02"),
    ("03", "03"),
    ("04", "04"),
    ("05", "05"),
    ("06", "06"),
    ("07", "07"),
    ("08", "08"),
    ("09", "09"),
    ("10", "10"),
    ("11", "11"),
    ("12", "12"),
  ]
  YEAR_CHOICES = [
    ("2020", "2020"),
    ("2021", "2021"),
    ("2022", "2022"),
    ("2023", "2023"),
    ("2024", "2024"),
    ("2025", "2025"),
    ("2026", "2026"),
    ("2027", "2027"),
    ("2028", "2028"),
    ("2029", "2029"),
    ("2030", "2030"),
    ("2031", "2031"),
    ("2032", "2032"),
    ("2033", "2033"),
    ("2034", "2034"),
  ]
  cc = forms.CharField(
    label="Card Number",
    max_length=16,
    widget=widgets.TextInput(attrs={"id": "cardNumber"}),
    required=False
  )
  expiry_month = forms.ChoiceField(
    label="Expiry Month",
    choices=MONTH_CHOICES,
    widget=widgets.Select(attrs={"id": "cardExpiryMonth"}),
    required=False
  )
  expiry_year = forms.ChoiceField(
    label="Expiry Year",
    choices=YEAR_CHOICES,
    widget=widgets.Select(attrs={"id": "cardExpiryYear"}),
    required=False
  )
  cvv = forms.CharField(
    label="CVV",
    max_length=4,
# id=cardCVV required for Helcim
    widget=widgets.TextInput(attrs={"id": "cardCVV"}),
    required=False
  )
  token = forms.CharField(
    widget=widgets.HiddenInput(attrs={
      "id": "token",
      "value": settings.HELCIM_API_TOKEN
    })
  )
  test = forms.CharField(
    widget=widgets.HiddenInput(attrs={
      "id": "test",
      "value": settings.HELCIM_TEST,
    })
  )
  card_holder_name = forms.CharField(
    widget=widgets.TextInput(attrs={"id": "cardHolderName"})
  )
  card_holder_address = forms.CharField(
    widget=widgets.TextInput(attrs={"id": "cardHolderAddress"})
  )
  card_holder_postal_code = forms.CharField(
    widget=widgets.TextInput(attrs={"id": "cardHolderPostalCode"})
  )
  amount = forms.CharField(
    widget=widgets.HiddenInput(attrs={
      "id": "amount",
      "value": "101.11"
    })
  )
# responses from Helcim.js
  cardNumber = forms.CharField(widget=widgets.HiddenInput())
  response = forms.CharField(widget=widgets.HiddenInput())
  responseMessage = forms.CharField(widget=widgets.HiddenInput())
  noticeMessage = forms.CharField(widget=widgets.HiddenInput())
  date = forms.DateField(widget=widgets.HiddenInput())
  time = forms.TimeField(widget=widgets.HiddenInput())
