from django.urls import path
from . import views

urlpatterns = [
  path("credit/<invoice_uuid>/", views.credit, name="credit_payment"),
  path("debit/<invoice_uuid>/", views.debit, name="debit_payment"),
]
