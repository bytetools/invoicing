import time
import os

from django.shortcuts import render
from django.http.response import HttpResponse, FileResponse
from django.template.loader import render_to_string
from django.conf import settings
from .models import Invoice, Address

def official_address_latex(name, addr):
  apt = ""
  number = ""
  name = name.upper()
  street = addr.street.upper()
  postal = addr.postal.upper()
  city = addr.municipality.name.upper()
  region = addr.municipality.region.short_name.upper()
  if addr.apt:
    apt_type = addr.apt_type.value if addr.apt_type else "UNIT"
    apt = f"{apt_type} {addr.apt}\\\\"
  if addr.number:
    number = f"{addr.number} "
  return f"{name}\\\\{apt}{number}{street}\\\\{city} {region} {postal}"

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

# Create your views here.
def index(request):
  inv = Invoice.objects.get(id=1)
  my_addr = Address.objects.get(id=2)
  total = sum([ii.total for ii in inv.items.all()])
  tax = total * 0.05
  final = total + tax
  tex_src = render_to_string("core/invoice.tex.tmpl", {
    "items": inv.items.all(),
    "comapny_name": "Bytetools Technologies Inc.",
    "company_address": official_address_latex("Bytetools Technologies Inc.", my_addr),
    "client_address": official_address_latex(inv.client.name, inv.client.address),
    "total": total,
    "tax": tax,
    "final": final,
    "company_logo_path":  "logo.png",
  })
  pdf = open(tex_to_pdf(tex_src), "rb")
  res = HttpResponse(pdf, content_type="application/pdf")
  res["Content-Disposition"] = "Test.pdf"
  return res
