import re
from django.urls import path, register_converter
from core.models import Product, Invoice
from . import views, converters

register_converter(converters.ActionConverter, "action")
register_converter(converters.ModelConverter, "model")

urlpatterns = [
  path("", views.index, name="index"),
  path("<action:action>/<model:model_name>/", views.action_on_model, name="action_on_model"),
  path("new/invoice/", views.new_invoice, name="new_invoice"),
#  path("list/invoice/", views.list_invoices, name="list_invoices"),
  path("new/client/", views.new_client, name="new_client"),
#  path("list/client/", views.list_clients, name="list_clients"),
  path("new/address/", views.new_address, name="new_address"),
#  path("list/address/", views.list_addresses, name="list_addresses"),
  path("new/country/", views.new_country, name="new_country"),
#  path("list/country/", views.list_countrys, name="list_countrys"),
  path("new/region/", views.new_region, name="new_region"),
#  path("list/region/", views.list_regions, name="list_regions"),
  path("new/city/", views.new_municipality, name="new_city"),
#  path("list/city/", views.list_municipalitys, name="list_citys"),
  path("new/tax/", views.new_tax, name="new_tax"),
#  path("list/tax/", views.list_taxes, name="list_taxes"),
#  path("new/product/", views.new_product, name="new_product"),
  path("list/product/", views.list_products, name="list_products"),
  path("pdf/<invoice_id>/", views.pdf, name="pdf"),
  path("html/<invoice_id>/", views.html, name="html"),
  path("txt/<invoice_id>/", views.txt, name="txt"),
  path("list/", views.list, name="list"),
]
