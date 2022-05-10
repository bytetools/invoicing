from datetime import datetime, date
import time
import os

from dateutil.relativedelta import relativedelta
from django.shortcuts import render, redirect
from django.http.response import HttpResponse, FileResponse
from django.template.loader import render_to_string
from django.template import RequestContext
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from .models import Invoice, Product
from accounts.models import Address
from .forms import InvoiceForm, InvoiceItemForm, AddressForm, CountryForm, RegionForm, MunicipalityForm, TaxForm, ProductForm, PaymentForm, CopyForm, DeleteForm
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
  os.system(f"pdflatex -interaction batchmode -output-directory {settings.PDF_AND_LATEX_ROOT} {tex_fname} {pdf_fname}")
  return pdf_fname

# take an AdditionalCharge, if percentage, then return percentage of subtotal; otherwise, return static charge amount
def _get_real_cost(subtotal, charge):
  return charge.amount if charge.charge_type == "F" else subtotal * charge.amount

def _get_real_amount(charge):
  return charge.amount if charge.charge_type == "F" else charge.amount * 100

# handles surcharges and discounts, but not taxes as they are technically different types in the DB. 
# TODO: migrate these to a common type
def _handle_charges(subtotal, amounts, negative=False):
  total = subtotal
  amount_objs = [{
    "cost": _get_real_cost(subtotal, a),
    "amount": _get_real_amount(a),
    "name": a.name,
    "charge_type": a.charge_type,
  } for a in amounts]
  difference = sum([x["cost"] for x in amount_objs])
  if negative:
    total -= difference
  else:
    total += difference
  return (total, amount_objs)

def _handle_taxes(subtotal, taxes):
  total = subtotal
  tax_objs = [{
    "cost": subtotal * t.percentage,
    "percentage": t.percentage * 100,
    "tax_type": t.tax_type,
    "identifier": t.identifier,
  } for t in taxes]
  total += sum([x["cost"] for x in tax_objs])
  return (total, tax_objs)

def _create_invoice_vars(invoice_uuid, request):
  inv = None
  my_addr = None
  try:
    inv = Invoice.objects.get(uuid=invoice_uuid)
  except:
    messages.add_message(request, messages.ERROR, "This is not a valid invoice.")
    return ({}, True)
  
  my_addr = inv.invoicer.address
  total = sum([ii.total() for ii in inv.items.all()])
  after_surcharge_total, surcharges = _handle_charges(total, inv.surcharges.all(), negative=False)
  after_discount_total, discounts = _handle_charges(after_surcharge_total, inv.discounts.all(), negative=True)
  final, taxes = _handle_taxes(after_discount_total, inv.taxes.all())

  client_address = official_address_latex(inv.client.name_on_invoice, inv.client.address).split("\\")
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
    "etransfer_email": inv.invoicer.email_on_invoice,
    "customer": inv.client,
    "company_name": "Bytetools Technologies Inc.",
    "company_address": official_address_latex("Bytetools Technologies Inc.", my_addr),
    "client_address": official_address_latex(inv.client.name_on_invoice, inv.client.address),
    "client_name": inv.client.name_on_invoice,
    "total": total,
    "surcharges": surcharges,
    "total_after_discounts": after_discount_total,
    "discounts": discounts,
    "taxes": taxes,
    "final": final,
    "company_logo_path":  "logo.png",
    "pay_debit_url": settings.BASE_URL + reverse_lazy("debit_payment", kwargs={"invoice_uuid": inv.uuid}),
    "pay_credit_url": settings.BASE_URL + reverse_lazy("credit_payment", kwargs={"invoice_uuid": inv.uuid}),
    "credit_surcharge_percentage": settings.CREDIT_SURCHARGE * 100,
  } | settings.INVOICE_VARS, False)

# Create your views here.
def pdf(request, invoice_uuid):
  invoice_vars, failed = _create_invoice_vars(invoice_uuid, request)
  if failed:
    return render(request, "core/index.html", {})
  tex_src = render_to_string("invoice/invoice.tex.tmpl", invoice_vars)
  pdf = open(tex_to_pdf(tex_src), "rb")
  res = HttpResponse(pdf, content_type="application/pdf")
  res["Content-Disposition"] = "Test.pdf"
  return res

def html(request, invoice_uuid):
  invoice_vars, failed = _create_invoice_vars(invoice_uuid, request)
  if failed:
    return render(request, "core/index.html", {})
  return render(request, "invoice/invoice.html", invoice_vars)

def txt(request, invoice_uuid):
  invoice_vars, failed = _create_invoice_vars(invoice_uuid, request)
  invoice_txt = None
  if failed:
    invoice_txt = render_to_string(request, "core/index.html", {})
  invoice_txt = render(request, "invoice/invoice.txt", invoice_vars)
  return HttpResponse(invoice_txt, content_type="text/plain")

def index(request):
    return render(request, "core/index.html",
        {"invoices": Invoice.objects.all()}
    )

@login_required
def list(request):
  return render(request, "core/invoice-list.html", {
    "invoices": Invoice.objects.all().order_by("-issued_on")
  })

@login_required
def add_invoice_item(request, invoice_uuid):
  form = InvoiceItemForm()
  invoice = None
  try:
    invoice = Invoice.objects.get(uuid=invoice_uuid)
    form = InvoiceItemForm(initial={"invoice": invoice.id})
  except Exception as e:
    messages.add_message(request, messages.ERROR, "Invoice not found")
  return render(request, "core/form.html", {
    "form": form
  })

@login_required
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

def _list(request, model, model_form):
  items = [{
    "update_form": model_form(instance=x),
    "delete_form": DeleteForm(initial={"uuid": x.uuid}),
    "copy_form": CopyForm(initial={"uuid": x.uuid})
  } for x in model.objects.all()]
  items.append({"update_form": model_form()})
  headers = map(lambda x: x.label, items[0]["update_form"].visible_fields())
  return render(request, "core/tablelist.html", {
    "items": items,
    "headers": headers
  })

def _model_and_form(model_name):
  return (
    MODEL_NAME_TO_MODEL[model_name],
    MODEL_NAME_TO_MODEL_FORM[model_name]
  )

@login_required
def read_model(request, model_name):
  model, model_form = _model_and_form(model_name)
  return _list(request, model, model_form)

@login_required
def create_model(request, model_name):
  model, model_form = _model_and_form(model_name)
  form = model_form(request.POST)
  if form.is_valid():
    form.save()
    messages.add_message(request, messages.SUCCESS, "New record created.")
  return redirect(reverse_lazy("read_model", kwargs={"model_name": model_name}))

@login_required
def update_model(request, model_name, model_uuid):
  model, model_form = _model_and_form(model_name)
  instance = model.objects.get(uuid=model_uuid)
  form = model_form(request.POST, instance=instance)
  if form.is_valid():
    form.save()
    messages.add_message(request, messages.SUCCESS, "Record updated")
  return redirect(reverse_lazy("read_model", kwargs={"model_name": model_name}))

@login_required
def delete_model(request, model_name, model_uuid):
  model = MODEL_NAME_TO_MODEL[model_name]
  form = DeleteForm(request.POST)
  if form.is_valid():
    instance = model.objects.get(uuid=model_uuid)
    instance.delete()
    messages.add_message(request, messages.SUCCESS, "Record deleted")
  return redirect(reverse_lazy("read_model", kwargs={"model_name": model_name}))

def payment(request):
  form = PaymentForm(request.POST or None)
  if form.is_valid():
    for k,v in form.cleaned_data.items():
      print(f"{k}: {v}")
  return render(request, "core/payment.html", {
    "helcim_js_config": settings.HELCIM_JS_CONFIG,
    "form": form
  })
