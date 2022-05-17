import datetime, uuid

from accounts.models import Address
from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
class Product(models.Model):
  uuid = models.UUIDField(default=uuid.uuid4, primary_key=False, unique=True, blank=False, null=False)
  cost = models.FloatField(blank=False, null=False)
  sku = models.CharField(max_length=8, blank=False, null=False, unique=True)
  name = models.CharField(max_length=128, blank=False, null=False)
  description = models.CharField(max_length=64, blank=True, null=False)
  note = models.CharField(max_length=32, blank=True)

  def __str__(self):
    return f"{self.sku}"

class AdditionalCharge(models.Model):
  CHARGE_TYPE_CHOICES = [
    ("P", "Percentage"),
    ("F", "Fixed"),
  ]
  uuid = models.UUIDField(default=uuid.uuid4, primary_key=False, unique=True, blank=False, null=False)
  name = models.CharField(max_length=32, blank=False, null=False)
  charge_type = models.CharField(max_length=1, choices=CHARGE_TYPE_CHOICES, blank=False, null=False)
  amount = models.FloatField(blank=False, null=False)

  class Meta:
    abstract = True

class Discount(AdditionalCharge):
  def __str__(self):
    if self.charge_type == "P":
      return f"{self.name} (-{self.amount*100}%)"
    else:
      return f"{self.name} (-${self.amount})"

class Surcharge(AdditionalCharge):
  def __str__(self):
    if self.charge_type == "P":
      return f"{self.name} (+{self.amount*100}%)"
    else:
      return f"{self.name} (+${self.amount})"

class Tax(models.Model):
  TAX_TYPE_CHOICES = [
    ("GST", "General Sales Tax"),
    ("HST", "Harmonized Sales Tax"),
    ("PST", "Provincial Sales Tax"),
    ("QST", "Quebec Sales Tax"),
  ]
  uuid = models.UUIDField(default=uuid.uuid4, primary_key=False, unique=True, blank=False, null=False)
  tax_type = models.CharField(max_length=3, choices=TAX_TYPE_CHOICES, blank=False, null=False)
  name = models.CharField(max_length=16, blank=False, null=False)
  percentage = models.FloatField(blank=False, null=False)
# tax identifier to show in invoice
  identifier = models.CharField(max_length=16, blank=False, null=False)

  def __str__(self):
    return f"{self.name}"

class Invoice(models.Model):
  uuid = models.UUIDField(default=uuid.uuid4, primary_key=False, unique=True, blank=False, null=False)
  issued_on = models.DateField(blank=False, null=False)
  due_date = models.DateField(blank=False, null=False)
  client = models.ForeignKey(get_user_model(), on_delete=models.PROTECT, related_name="incoming_invoices", blank=False, null=False)
  invoicer = models.ForeignKey(get_user_model(), on_delete=models.PROTECT, related_name="outgoing_invoices", blank=False, null=False)
  taxes = models.ManyToManyField(Tax, related_name="invoices", blank=True)
  discounts = models.ManyToManyField(Discount, related_name="invoices", blank=True)
  surcharges = models.ManyToManyField(Surcharge, related_name="invoices", blank=True)

  def __str__(self):
    return f"{self.client.name_on_invoice} #{self.id} ({self.issued_on})"

class InvoiceItem(models.Model):
  uuid = models.UUIDField(default=uuid.uuid4, primary_key=False, unique=True, blank=False, null=False)
  invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name="items")
  product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name="invoices")
  quantity = models.FloatField()
  notes = models.CharField(max_length=256, blank=True, null=False, default="")

  def total(self):
    return self.product.cost * self.quantity

class InvoiceFile(models.Model):
  FILE_TYPE = [
    ("P", "PDF"),
    ("T", "TXT"),
    ("C", "CSV"),
    ("H", "HTML"),
  ]
  uuid = models.UUIDField(default=uuid.uuid4, primary_key=False, unique=True, blank=False, null=False)
  invoice = models.ForeignKey(Invoice, blank=False, null=False, on_delete=models.PROTECT)
  file = models.FileField(blank=False, null=False)
  file_type = models.CharField(max_length=1, choices=FILE_TYPE, blank=False, null=False, editable=False)
