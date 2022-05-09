from django import template

register = template.Library()

@register.filter(name="dollar")
def dollar(amount):
  return f"{amount:.2f}"
