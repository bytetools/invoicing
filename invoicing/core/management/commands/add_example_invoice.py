import datetime
from datetime import date
from dateutil.relativedelta import relativedelta
from django.core.management.base import BaseCommand, CommandError
from core.models import *

class Command(BaseCommand):
  help = "Populate the database with an example invoice."

  def load_invoice(self):
    tax = Tax.objects.filter(tax_type="GST")[0]
    tax2 = Tax.objects.filter(tax_type="PST")[0]
    discount_1 = Discount.objects.create(
      name="Small Business Discount",
      discount_type="P", # percentage discount
      amount=0.1 # 10%
    )
    discount_2 = Discount.objects.create(
      name="New Client Discount",
      discount_type="F", # fixed discount
      amount=50 # $50
    )
    ca = Country.objects.create(name="Canada", short_name="CA")
    ab = Region.objects.create(name="Alberta", short_name="AB", country=ca)
    bc = Region.objects.create(name="British Columbia", short_name="BC", country=ca)
    cgy = Municipality.objects.create(name="Calgary", region=ab)
    brn = Municipality.objects.create(name="Burnaby", region=bc)
    addr = Address.objects.create(
      municipality=cgy,
      street="PO Box 12062 RPO Copperfield",
      postal="T2Z 1H4"
    )
    addr_sfu = Address.objects.create(
      municipality=brn,
      apt=1500,
      apt_type="R",
      street="Maggie Benston Center, Simon Fraser University",
      postal="V5A 1S6"
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
      name="Simon Fraser University",
      address=addr_sfu,
    )
    invoicer = Invoicer.objects.create(
      name="Bytetools Technologies Inc.",
      address=my_addr,
    )

    inv = Invoice.objects.create(
      client=client,
      invoicer=invoicer,
      issued_on=date.today(),
      due_date=date.today() - relativedelta(months=1)
    )
    inv.taxes.set([tax, tax2])
    inv.discounts.set([discount_1, discount_2])
    inv.save()
    infos = [
      ("SCRIBE", "Transcription for CMPT 215 (week 5)", 35, 12, 35*12),
      ("SCRIBE", "Transcription for CMPT 218 (week 5)", 35, 100, 35*100),
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
