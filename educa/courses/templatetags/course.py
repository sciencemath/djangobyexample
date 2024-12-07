from django import template

register = template.Library()

@register.filter
def model_name(obj):
  """
  Creating a custom template filter because accessing
  _meta is not allowed Python will assume its private
  """
  try:
    return obj._meta.model_name
  except AttributeError:
    return None