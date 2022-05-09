import re
from django.urls import path, register_converter
from core.models import Product, Invoice
from . import views, converters

register_converter(converters.ModelConverter, "model")

urlpatterns = [
  path("", views.index, name="index"),
  path("read/<model:model_name>/", views.read_model, name="read_model"),
  path("create/<model:model_name>/", views.create_model, name="create_model"),
  path("update/<model:model_name>/<model_uuid>/", views.update_model, name="update_model"),
  path("delete/<model:model_name>/<model_uuid>/", views.delete_model, name="delete_model"),
  path("pdf/<invoice_uuid>/", views.pdf, name="pdf"),
  path("html/<invoice_uuid>/", views.html, name="html"),
  path("txt/<invoice_uuid>/", views.txt, name="txt"),
  path("payment/", views.payment, name="payment"),
  path("list/", views.list, name="list"),
]
