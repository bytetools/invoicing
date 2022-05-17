from django.db import models
from django.contrib.auth import get_user_model

from invoices.models import Invoice

# Create your models here.
class EmailAttempt(models.Model):
  EMAIL_STATUS_CHOICES = [
    ("C", "Created"),
    ("S", "Success"),
    ("F", "Failure"),
  ]
  recipients = models.ManyToManyField(get_user_model(), related_name="emails_attempted_to", blank=True)
  cc_recipients = models.ManyToManyField(get_user_model(), related_name="emails_attempted_cc_to", blank=True)
  bcc_recipients = models.ManyToManyField(get_user_model(), related_name="email_attempted_bcc_to", blank=True)
  invoice = models.ForeignKey(Invoice, related_name="email_attempts", on_delete=models.PROTECT)
  timestamp = models.DateTimeField(auto_now=True, editable=False)
  status = models.CharField(max_length=1, choices=EMAIL_STATUS_CHOICES, default="C")
