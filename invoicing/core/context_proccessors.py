from invoices.converters import MODEL_NAMES

def nav(request):
  nav_dict = {
    "model_names": MODEL_NAMES,
  }
  return nav_dict
