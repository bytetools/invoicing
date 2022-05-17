from django import template

register = template.Library()

ESCAPE_LIST = [
  "#", "%", "&",
]

@register.filter(name="tex_safe")
def tex_safe(string):
  final_string = string
  for escape_char in ESCAPE_LIST:
    final_string = final_string.replace(escape_char, "\\" + escape_char)
  print(final_string)
  return final_string
