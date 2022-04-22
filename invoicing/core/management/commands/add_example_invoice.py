from django.core.management.base import BaseCommand, CommandError
from core.models import *

class Command(BaseCommand):
  help = "Populate the database with an example invoice."

  def load_invoice(self):
    ca = Country.objects.create(name="Canada", short_name="CA")
    ab = Region.objects.create(name="Alberta", short_name="AB", country=ca)
    cgy = Municipality.objects.create(name="Calgary", region=ab)
    addr = Address.objects.create(
      municipality=cgy,
      street="PO Box 12062 RPO Copperfield",
      postal="T2Z 1H4"
    )
    my_addr = Address.objects.create(
      municipality=cgy,
      street="Edmonton Trail NE",
      number=611,
      apt=501,
      apt_type="U",
      postal="T2E 3J3"
    )
    client = Client.objects.create(
      name="Bahn Projects",
      address=addr,
    )

    inv = Invoice.objects.create(
      client=client
    )
    inv.save()
    infos = [
      ("SCRIBE", "Transcription for CMPT 215 (week 5)", 35, 12, 35*12),
      ("SCRIBE", "Transcription for CMPT 218 (week 5)", 35, 2, 35*2),
      ("SCRIBE", "Transcription for LING 200 (week 5)", 35, 5, 35*5),
    ]
    for info in infos:
      invitem = InvoiceItem.objects.create(
        invoice=inv,
        sku=info[0],
        description=info[1],
        cost=info[2],
        quantity=info[3],
        total=info[4]
      )
      invitem.save()
    print(inv)
    print(inv.items.all())

  def handle(self, *args, **kwargs):
    self.stdout.write("Loading database with an invoice... ")
    self.load_invoice()
    self.stdout.write(self.style.SUCCESS("Example invoice sucessfully added."))
