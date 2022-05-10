import datetime
from datetime import date
from dateutil.relativedelta import relativedelta
from django.core.management.base import BaseCommand, CommandError
from core.models import *
from accounts.models import *

class Command(BaseCommand):
  help = "Populate the database with an example invoice."

  def load_invoice(self):
    tax = Tax.objects.filter(tax_type="GST")[0]
    tax2 = Tax.objects.filter(tax_type="PST")[0]
    surcharge_1 = Surcharge.objects.create(
      name="Off Hours Work",
      charge_type="P",
      amount=0.50, # 50% surcharge
    )
    surcharge_2 = Surcharge.objects.create(
      name="Starting Charge",
      charge_type="F",
      amount=75.00, # $75 to start work when on call
    )
    discount_1 = Discount.objects.create(
      name="Small Business Discount",
      charge_type="P", # percentage discount
      amount=0.1 # 10%
    )
    discount_2 = Discount.objects.create(
      name="New Client Discount",
      charge_type="F", # fixed discount
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
    sfu = get_user_model().objects.create(
      username="sfu",
      is_active=False,
      name_on_invoice="Simon Fraser University",
      address=addr_sfu,
    )
    btti = get_user_model().objects.create(
      username="btt",
      is_active=False,
      name_on_invoice="Bytetools Technologies Inc.",
      email_on_invoice="finances@bytetools.ca",
      address=my_addr
    )
    inv = Invoice.objects.create(
      client=sfu,
      invoicer=btti,
      issued_on=date.today(),
      due_date=date.today() + relativedelta(months=1)
    )
    inv.taxes.set([tax, tax2])
    inv.discounts.set([discount_1, discount_2])
    inv.surcharges.set([surcharge_1, surcharge_2])
    inv.save()
    infos = [
      ("SCRIBE", "CMPT 215 (week 5)", 35, 12, 35*12),
      ("SCRIBE", "CMPT 218 (week 5)", 35, 100, 35*100),
      ("SCRIBE", "LING 200 (week 5)", 35, 5, 35*5),
    ]
    product = Product.objects.create(
            name="ALT Format Transcription",
            description="Alternate Format Transcription",
            sku="SCRIBE",
            cost=35,
    )
    product.save()
    for info in infos:
      invitem = InvoiceItem.objects.create(
        invoice=inv,
        product=product,
        notes=info[1],
        quantity=info[3]
      )
      invitem.save()
    print(inv)
    print(inv.items.all())

  def handle(self, *args, **kwargs):
    self.stdout.write("Loading database with an invoice... ")
    self.load_invoice()
    self.stdout.write(self.style.SUCCESS("Example invoice sucessfully added."))
