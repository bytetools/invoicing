import uuid

from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class NotificationType(models.Model):
  NOTIFICATION_CHOICES = [
    ("T", "Text Message"),
    ("E", "Email"),
  ]
  uuid = models.UUIDField(default=uuid.uuid4, primary_key=False, unique=False, blank=False, null=False)
  name = models.CharField(max_length=1, blank=False, null=False, editable=False)
  def __str__(self):
    for (k,v) in self.NOTIFICATION_CHOICES:
      if k == self.name:
        return v
    return "N/A"

class Country(models.Model):
  uuid = models.UUIDField(default=uuid.uuid4, primary_key=False, unique=False, blank=False, null=False)
  name = models.CharField(max_length=64)
  short_name = models.CharField(max_length=4)

  def __str__(self):
    return f"{self.name}"

class Region(models.Model):
  uuid = models.UUIDField(default=uuid.uuid4, primary_key=False, unique=False, blank=False, null=False)
  country = models.ForeignKey(Country, on_delete=models.PROTECT, related_name="regions")
  name = models.CharField(max_length=64)
  short_name = models.CharField(max_length=4)
  def __str__(self):
    return f"{self.name}, {self.country}"

class Municipality(models.Model):
  uuid = models.UUIDField(default=uuid.uuid4, primary_key=False, unique=False, blank=False, null=False)
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
    uuid = models.UUIDField(default=uuid.uuid4, primary_key=False, unique=False, blank=False, null=False)
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

class InvoiceUser(AbstractUser):
  uuid = models.UUIDField(default=uuid.uuid4, primary_key=False, unique=False, blank=False, null=False)
  phone = PhoneNumberField(blank=True, null=True)
  name_on_invoice = models.CharField(max_length=32, blank=False, null=False, default="")
  email_on_invoice = models.EmailField(max_length=32, blank=False, null=False, default="")
  address = models.ForeignKey(Address, blank=True, null=True, on_delete=models.PROTECT, related_name="users")
  new_invoice_notification = models.ManyToManyField(NotificationType, default=[], blank=True, related_name="new_invoice_users")
  invoice_due_notification = models.ManyToManyField(NotificationType, default=[], blank=True, related_name="invoice_due_users")
  def __str__(self):
    return self.username
