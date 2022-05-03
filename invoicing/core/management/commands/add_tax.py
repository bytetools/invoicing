from django.core.management.base import BaseCommand, CommandError
from core.models import Tax

class Command(BaseCommand):
  help = "Populate the database with an example invoice."

  def load_taxes(self):
    TAXES = [
      ("GST", 0.05, "GST (Canada)", "CRxxxxxxxxxxx"),
      ("PST", 0.07, "PST (BC)", "BCPxxxxxxxxx"),
    ]
    for tax in TAXES:
      Tax.objects.create(
        tax_type=tax[0],
        percentage=tax[1],
        name=tax[2],
        identifier=tax[3]
      )

  def handle(self, *args, **kwargs):
    self.stdout.write("Loading database with tax types... ")
    self.load_taxes()
    self.stdout.write(self.style.SUCCESS("Tax options successfully added."))
