from django import template

register = template.Library()

# return integer if float has an integer value, else return float
# this makes percentages display with no decimal when not necessary
@register.filter(name="percentage")
def percentage(flt):
# remove rounding errors from binary storage; i.e., 7.00000001, but still allowing tiny points like a specialty tax on specific goods, i.e.,  0.1275% on certain foods, etc.
  flt = round(flt, 5)
  return int(flt) if int(flt) == flt else flt
