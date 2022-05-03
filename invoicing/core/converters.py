import re
from core.models import Product, Invoice
from core.forms import ProductForm, InvoiceForm

ACTIONS = [
  "list",
  "new",
  "copy",
  "delete"
]

MODELS = [
  Product,
  Invoice
]

MODEL_FORMS = [
  ProductForm,
  InvoiceForm
]

MODEL_NAMES = [x.__name__.lower() for x in MODELS]
MODEL_NAME_TO_MODEL = dict(zip(MODEL_NAMES, MODELS))
MODEL_NAME_TO_MODEL_FORM = dict(zip(MODEL_NAMES, MODEL_FORMS))

class ActionConverter:
    _actions = "|".join(ACTIONS)
    regex = f"({_actions})"

    def to_python(self, value):
        result = re.match(self.regex, value)
        return result.group() if result is not None else ""

    def to_url(self, value):
        result = re.match(self.regex, value)
        return result.group() if result is not None else ""

class ModelConverter:
    _models = "|".join(MODEL_NAMES)
    regex = f"({_models})"

    def to_python(self, value):
        result = re.match(self.regex, value)
        return result.group() if result is not None else ""

    def to_url(self, value):
        result = re.match(self.regex, value)
        return result.group() if result is not None else ""
