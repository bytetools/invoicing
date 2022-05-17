import re
from invoices.models import Product, Invoice, InvoiceItem, Tax, Address
from invoices.forms import ProductForm, InvoiceForm, InvoiceItemForm, TaxForm, AddressForm, CountryForm, RegionForm, MunicipalityForm
from accounts.models import Country, Region, Municipality

MODELS = [
  Product,
  InvoiceItem,
  Invoice,
  Tax,
  Address,
  Country,
  Region,
  Municipality
]

MODEL_FORMS = [
  ProductForm,
  InvoiceItemForm,
  InvoiceForm,
  TaxForm,
  AddressForm,
  CountryForm,
  RegionForm,
  MunicipalityForm
]

MODEL_NAMES = [x.__name__.lower() for x in MODELS]
MODEL_NAME_TO_MODEL = dict(zip(MODEL_NAMES, MODELS))
MODEL_NAME_TO_MODEL_FORM = dict(zip(MODEL_NAMES, MODEL_FORMS))

class ModelConverter:
    _models = "|".join(MODEL_NAMES)
    regex = f"({_models})"

    def to_python(self, value):
        result = re.match(self.regex, value)
        return result.group() if result is not None else ""

    def to_url(self, value):
        result = re.match(self.regex, value)
        return result.group() if result is not None else ""
