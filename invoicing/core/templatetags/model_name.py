from django import template

register = template.Library()

@register.filter(name="model_name")
def model_name(model):
  name = model._meta.model.__name__.lower()
  return f"{name}"
