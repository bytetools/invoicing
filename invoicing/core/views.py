from datetime import datetime, date
import time
import os

from dateutil.relativedelta import relativedelta
from django.shortcuts import render
from django.http.response import HttpResponse, FileResponse
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib import messages
from .models import Invoice, Address, Product
from .forms import InvoiceForm, InvoiceItemForm, ClientForm, AddressForm, CountryForm, RegionForm, MunicipalityForm, TaxForm, ProductForm
from .converters import MODEL_NAME_TO_MODEL, MODEL_NAME_TO_MODEL_FORM

def official_address_latex(name, addr):
  apt = ""
  number = ""
  name = name.upper()
  street = addr.street.upper()
  postal = addr.postal.upper()
  city = addr.municipality.name.upper()
  region = addr.municipality.region.short_name.upper()
  if addr.apt:
    apt_type = addr.get_apt_type_display().upper() if addr.apt_type else "UNIT"
    apt = f"{apt_type} {addr.apt}\\"
  if addr.number:
    number = f"{addr.number} "
  return f"{apt}{number}{street}\\{city} {region} {postal}"

def tex_to_pdf(tex_src):
  cur_time = time.localtime()
  cur_time_fname = time.strftime("%Y%m%d%h%m%s", cur_time)
  tex_fname = f"{settings.PDF_AND_LATEX_ROOT}/tmp-{cur_time_fname}.tex"
  pdf_fname = f"{settings.PDF_AND_LATEX_ROOT}/tmp-{cur_time_fname}.pdf"
# if dir does not exist, create it
  if not os.path.isdir(settings.PDF_AND_LATEX_ROOT):
    os.mkdir(settings.PDF_AND_LATEX_ROOT)
  tex_file = open(tex_fname, "w")
  tex_file.write(tex_src)
  tex_file.close()
  os.system(f"pdflatex -output-directory {settings.PDF_AND_LATEX_ROOT} {tex_fname} {pdf_fname}")
  return pdf_fname

def _create_invoice_vars(invoice_id, request):
  inv = None
  my_addr = None
  try:
    inv = Invoice.objects.get(id=invoice_id)
  except:
    messages.add_message(request, messages.ERROR, "This is not a valid invoice.")
    return ({}, True)
  
  my_addr = inv.invoicer.address
  total = sum([ii.total for ii in inv.items.all()])
  discounts = [
    {"cost": total*discount.amount if discount.discount_type == "P" else discount.amount,
      "name": discount.name,
      "amount": discount.amount * 100 if discount.discount_type == "P" else discount.amount,
      "discount_type": discount.discount_type} 
  for discount in inv.discounts.all()]
  discount_costs = [d["cost"] for d in discounts]
  after_discount_total = total - sum(discount_costs)
  tax_costs = [after_discount_total * tax.percentage for tax in inv.taxes.all()]
  taxes = [{"cost": after_discount_total * tax.percentage, "tax_type": tax.tax_type, "identifier": tax.identifier, "percentage": tax.percentage * 100} for tax in inv.taxes.all()]
  final = after_discount_total + sum(tax_costs)
  client_address = official_address_latex(inv.client.name, inv.client.address).split("\\")
  company_address = official_address_latex("Bytetools Technologies Inc.", my_addr).split("\\")
  address_lines = [("" if len(company_address) <= i else company_address[i], "" if len(client_address) <= i else client_address[i]) for i in range(max([len(client_address), len(company_address)]))]
  invoice_datetime = datetime.combine(inv.issued_on, datetime.min.time())
  invoice_due_date_datetime = datetime.combine(inv.due_date, datetime.min.time())
  invoice_datetime_formatted = invoice_datetime.strftime("%Y-%m-%d")
  invoice_due_date_datetime_formatted = invoice_due_date_datetime.strftime("%Y-%m-%d")
  invoice_number = inv.id
  return ({
    "address_lines": address_lines,
    "items": inv.items.all(),
    "invoice_date": invoice_datetime_formatted,
    "invoice_due_date": invoice_due_date_datetime_formatted,
    "invoice_number": invoice_number,
    "customer": inv.client,
    "company_name": "Bytetools Technologies Inc.",
    "company_address": official_address_latex("Bytetools Technologies Inc.", my_addr),
    "client_address": official_address_latex(inv.client.name, inv.client.address),
    "client_name": inv.client.name,
    "total": total,
    "total_after_discounts": after_discount_total,
    "discounts": discounts,
    "taxes": taxes,
    "final": final,
    "company_logo_path":  "logo.png",
  } | settings.INVOICE_VARS, False)

# Create your views here.
def pdf(request, invoice_id):
  invoice_vars, failed = _create_invoice_vars(invoice_id, request)
  if failed:
    return render(request, "core/index.html", {})
  tex_src = render_to_string("core/invoice.tex.tmpl", invoice_vars)
  pdf = open(tex_to_pdf(tex_src), "rb")
  res = HttpResponse(pdf, content_type="application/pdf")
  res["Content-Disposition"] = "Test.pdf"
  return res

def html(request, invoice_id):
  invoice_vars, failed = _create_invoice_vars(invoice_id, request)
  if failed:
    return render(request, "core/index.html", {})
  return render(request, "core/invoice-html.html", invoice_vars)

def txt(request, invoice_id):
  invoice_vars, failed = _create_invoice_vars(invoice_id, request)
  invoice_txt = None
  if failed:
    invoice_txt = render_to_string(request, "core/index.html", {})
  invoice_txt = render(request, "core/invoice.txt.tmpl", invoice_vars)
  return HttpResponse(invoice_txt, content_type="text/plain")

def index(request):
  return render(request, "core/index.html", {})

def list(request):
  return render(request, "core/invoice-list.html", {
    "invoices": Invoice.objects.all().order_by("-issued_on")
  })

def add_invoice_item(request, invoice_id):
  form = InvoiceItemForm()
  invoice = None
  try:
    invoice = Invoice.objects.get(id=invoice_id)
    form = InvoiceItemForm(initial={"invoice": invoice.id})
  except Exception as e:
    messages.add_message(request, messages.ERROR, "Invoice not found")
  return render(request, "core/form.html", {
    "form": form
  })

def new_invoice(request):
  form = InvoiceForm(initial={
    "issued_on": date.today(),
    "due_date": date.today() - relativedelta(months=1),
  })
  invoice = None
  if request.method == "POST":
    form = InvoiceForm(request.POST)
    if not form.is_valid():
      messages.add_message(request, messages.ERROR, "Form is invalid")
      return render(request, "core/form.html", {
        "form": form,
      })
    try:
      invoice = form.save()
      messages.add_message(request, messages.SUCCESS, "New Invoice Created")
    except Exception as e:
      messages.add_message(request, messages.ERROR, "Unable to save form")
      return render(request, "core/form.html", {"form": form})
    return add_invoice_item(request, invoice.id)
  return render(request, "core/form.html", {
    "form": form,
  })

def _form(request, form_obj, success_msg="Successfully saved!"):
  form = form_obj()
  if request.method == "POST":
    form = form_obj(request.POST)
    if not form.is_valid():
      messages.add_message(request, messages.ERROR, "The form is not valid.")
      return render(request, "core/form.html", {
        "form": form
      })
    try:
      form.save()
      messages.add_message(request, messages.SUCCESS, success_msg)
    except Exception as e:
      messages.add_message(request, messages.ERROR, "The form could not be saved.")
  return render(request, "core/form.html", {
    "form": form
  })

def new_client(request):
  return _form(request, ClientForm)

def new_address(request):
  return _form(request, AddressForm)

def new_country(request):
  return _form(request, CountryForm)

def new_region(request):
  return _form(request, RegionForm)

def new_municipality(request):
  return _form(request, MunicipalityForm)

def new_tax(request):
  return _form(request, TaxForm)

def new_product(request):
  return _form(request, ProductForm)

def _list(request, model, model_form):
  items = [model_form(instance=x) for x in model.objects.all()]
  items.append(model_form())
  headers = [x.label for x in items[0]]
  return render(request, "core/tablelist.html", {
    "items": items,
    "headers": headers
  })

def list_products(request):
  return _list(request, Product, ProductForm)

def action_on_model(request, action, model_name):
# model, model_form should never fail to find the associated variable because it is autogenerated and made part of the URL. Check core.converters and core.urls for more info. 
  model = MODEL_NAME_TO_MODEL[model_name]
  model_form = MODEL_NAME_TO_MODEL_FORM[model_name]
  items = [model_form(instance=x) for x in model.objects.all()]
  items.append(model_form())
  headers = [x.label for x in items[0]]
  return render(request, "core/tablelist.html", {
    "items": items,
    "headers": headers
  })
