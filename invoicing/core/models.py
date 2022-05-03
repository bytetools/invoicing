import datetime
from django.db import models

# Create your models here.

class Country(models.Model):
  name = models.CharField(max_length=64)
  short_name = models.CharField(max_length=4)

  def __str__(self):
    return f"{self.name}"

class Region(models.Model):
  country = models.ForeignKey(Country, on_delete=models.PROTECT, related_name="regions")
  name = models.CharField(max_length=64)
  short_name = models.CharField(max_length=4)
  def __str__(self):
    return f"{self.name}, {self.country}"

class Municipality(models.Model):
  name = models.CharField(max_length=32)
  region = models.ForeignKey(Region, on_delete=models.PROTECT, related_name="municipalities")
  def __str__(self):
    return f"{self.name}, {self.region}"

class Address(models.Model):
    APT_CHOICES = (
      ("U", "Unit"),
      ("S", "Suite"),
      ("A", "Apt"),
      ("R", "Room"),
    )

    street = models.CharField(max_length=50)
    municipality = models.ForeignKey(Municipality, on_delete=models.PROTECT, related_name="addresses")
    number = models.IntegerField(blank=True, null=True)
# TODO: validate both apt and apt_type are set together
    apt_type = models.CharField(blank=True, null=True, choices=APT_CHOICES, max_length=1)
    apt = models.IntegerField(blank=True, null=True)
# TODO: validate based on country
    postal = models.CharField(max_length=8)

    def __str__(self):
      num = self.number if self.number else ""
      return f"{num} {self.street} {self.postal}"

class Invoicer(models.Model):
  name = models.CharField(max_length=100)
  address = models.ForeignKey(Address, on_delete=models.PROTECT, related_name="companies", null=False, blank=False, editable=False)
  def __str__(self):
    return f"{self.name}"

class Client(models.Model):
  name = models.CharField(max_length=100)
  address = models.ForeignKey(Address, on_delete=models.PROTECT, related_name='clients', null=False, blank=False)
  def __str__(self):
    return f"{self.name}"

class Product(models.Model):
  cost = models.FloatField(blank=False, null=False)
  sku = models.CharField(max_length=8, blank=False, null=False)
  name = models.CharField(max_length=128, blank=False, null=False)
  description = models.CharField(max_length=64, blank=True, null=False)
  note = models.CharField(max_length=32, blank=True)

  def __str__(self):
    return f"{self.name}"

class Discount(models.Model):
  DISCOUNT_TYPE_CHOICES = [
    ("P", "Percentage"),
    ("F", "Fixed"),
  ]
  name = models.CharField(max_length=32, blank=False, null=False)
  discount_type = models.CharField(max_length=1, choices=DISCOUNT_TYPE_CHOICES, blank=False, null=False)
  amount = models.FloatField(blank=False, null=False)

  def __str__(self):
    if self.discount_type == "P":
      return f"{self.name} (-{self.amount*100}%)"
    else:
      return f"{self.name} (-${self.amount})"

class Tax(models.Model):
  TAX_TYPE_CHOICES = [
    ("GST", "General Sales Tax"),
    ("HST", "Harmonized Sales Tax"),
    ("PST", "Provincial Sales Tax"),
    ("QST", "Quebec Sales Tax"),
  ]
  tax_type = models.CharField(max_length=3, choices=TAX_TYPE_CHOICES, blank=False, null=False)
  name = models.CharField(max_length=16, blank=False, null=False)
  percentage = models.FloatField(blank=False, null=False)
# tax identifier to show in invoice
  identifier = models.CharField(max_length=16, blank=False, null=False)

  def __str__(self):
    return f"{self.name}"

class Invoice(models.Model):
  issued_on = models.DateField(blank=False, null=False)
  due_date = models.DateField(blank=False, null=False)
  client = models.ForeignKey(Client, on_delete=models.PROTECT, related_name="invoices", blank=False, null=False)
  invoicer = models.ForeignKey(Invoicer, on_delete=models.PROTECT, related_name="invoices", blank=False, null=False)
  taxes = models.ManyToManyField(Tax, related_name="invoices", blank=True)
  discounts = models.ManyToManyField(Discount, related_name="invoices", blank=True)

  def __str__(self):
    return f"{self.client} #{self.id} ({self.issued_on})"

class InvoiceItem(models.Model):
  invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name="items")
  name = models.CharField(max_length=128)
  description = models.CharField(max_length=128)
  sku = models.CharField(max_length=8)
  cost = models.FloatField()
  quantity = models.FloatField()
  total = models.FloatField()
  notes = models.CharField(max_length=256, blank=True, null=False, default="")

class InvoiceFile(models.Model):
  FILE_TYPE = [
    ("P", "PDF"),
    ("T", "TXT"),
    ("C", "CSV"),
    ("H", "HTML"),
  ]
  invoice = models.ForeignKey(Invoice, blank=False, null=False, on_delete=models.PROTECT, editable=False)
  file = models.FileField(blank=False, null=False, max_length=10*1024*1024)
  file_type = models.CharField(max_length=1, choices=FILE_TYPE, blank=False, null=False, editable=False)
