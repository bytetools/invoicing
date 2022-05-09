import uuid

from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.
class HelcimBaseTransaction(models.Model):
  uuid = models.UUIDField(default=uuid.uuid4, primary_key=False, unique=False, blank=False, null=False)
  token = models.CharField(max_length=32, blank=False, null=False)
  test = models.BooleanField(blank=False, null=False, default=False)
  amount = models.FloatField(blank=False, null=False)
  response = models.BooleanField(blank=False, null=False)
  response_message = models.CharField(max_length=12, blank=False, null=False)
  date = models.DateField(blank=False, null=False)
  time = models.TimeField(blank=False, null=False)
  notice_message = models.CharField(max_length=64, blank=False, null=False)
  type = models.CharField(max_length=16, blank=False, null=False)
  transaction_id = models.CharField(max_length=12, blank=False, null=False)
  order_number = models.CharField(max_length=12, blank=False, null=False)
  customer_code = models.CharField(max_length=8, blank=False, null=False)
  currency = models.CharField(max_length=3, blank=False, null=False)
  class Meta:
    abstract = True

class HelcimDebitTransaction(HelcimBaseTransaction):
  BANK_ACCOUNT_TYPE_CHOICES = [
    ("CHK", "Chequing"),
    ("SAV", "Savings")
  ]
  BANK_ACCOUNT_CORPORATE_CHOICES = [
    ("P", "Personal"),
    ("C", "Corporate")
  ]
  user = models.ForeignKey(get_user_model(), blank=True, null=True, related_name="debit_transactions", on_delete=models.PROTECT)
  bank_account_type = models.CharField(max_length=3, choices=BANK_ACCOUNT_TYPE_CHOICES, blank=False, null=False)
  bank_account_corporate = models.CharField(max_length=1, choices=BANK_ACCOUNT_CORPORATE_CHOICES, blank=False, null=False)
  bank_account_token = models.CharField(max_length=12, blank=False, null=False)
  bank_financial_number = models.CharField(max_length=8, blank=False, null=False)
  bank_transit_number = models.CharField(max_length=8, blank=False, null=False)
  bank_account_number = models.CharField(max_length=20, blank=False, null=False)

class HelcimCreditTransaction(HelcimBaseTransaction):
  user = models.ForeignKey(get_user_model(), blank=True, null=True, related_name="credit_transactions", on_delete=models.PROTECT)
  card_holder_name = models.CharField(max_length=32, blank=False, null=False)
  card_holder_address = models.CharField(max_length=32, blank=False, null=False)
  card_holder_postal_code = models.CharField(max_length=8, blank=False, null=False)
  card_number = models.CharField(max_length=22, blank=False, null=False)
  avs_response = models.CharField(max_length=1, blank=False, null=False)
  cvv_response = models.CharField(max_length=1, blank=False, null=False)
  approval_code = models.CharField(max_length=12, blank=False, null=False)
