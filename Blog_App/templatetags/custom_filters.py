from django import template

register = template.Library()

@register.filter
def range_filter(tekst):
    return tekst[0:500] + ".."



