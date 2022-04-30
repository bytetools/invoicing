from django.db import models

# Create your models here.

class Country(models.Model):
  name = models.CharField(max_length=64)
  short_name = models.CharField(max_length=4)

class Region(models.Model):
  country = models.ForeignKey(Country, on_delete=models.PROTECT, related_name="regions")
  name = models.CharField(max_length=64)
  short_name = models.CharField(max_length=4)

class Municipality(models.Model):
  name = models.CharField(max_length=32)
  region = models.ForeignKey(Region, on_delete=models.PROTECT, related_name="municipalities")

class Address(models.Model):
    APT_CHOICES = (
      ("U", "Unit"),
      ("S", "Suite"),
      ("A", "Apt"),
    )

    street = models.CharField(max_length=50)
    municipality = models.ForeignKey(Municipality, on_delete=models.PROTECT, related_name="addresses")
    number = models.IntegerField(blank=True, null=True)
# TODO: validate both apt and apt_type are set together
    apt_type = models.CharField(blank=True, null=True, choices=APT_CHOICES, max_length=1)
    apt = models.IntegerField(blank=True, null=True)
# TODO: validate based on country
    postal = models.CharField(max_length=8)

class Client(models.Model):
    name = models.CharField(max_length=100)
    address = models.ForeignKey(Address, on_delete=models.PROTECT, related_name='clients', null=False, blank=False)

class Service(models.Model):
    cost = models.FloatField()
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

class Product(models.Model):
  cost = models.FloatField(editable=False)
  sku = models.CharField(max_length=8, editable=False)
  name = models.CharField(max_length=128, editable=False)
  comment = models.CharField(max_length=32, editable=False)

class Invoice(models.Model):
  issued_on = models.DateField(auto_now=True, editable=False, blank=False, null=False)
  client = models.ForeignKey(Client, on_delete=models.PROTECT, related_name="invoices", blank=False, null=False)

class InvoiceItem(models.Model):
  invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name="items", editable=False)
  name = models.CharField(max_length=128, editable=False)
  description = models.CharField(max_length=128, editable=False)
  sku = models.CharField(max_length=8, editable=False)
  cost = models.FloatField(editable=False)
  quantity = models.FloatField(editable=False)
  total = models.FloatField(editable=False)
  notes = models.CharField(max_length=256, blank=True, null=False, default="")
