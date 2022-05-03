from django import template

register = template.Library()

@register.filter(name="tex_safe")
def tex_safe(string):
  return string.replace("#", "\\#").replace("%", "\\%")
