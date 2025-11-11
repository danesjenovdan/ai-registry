from django import template

register = template.Library()


@register.filter
def filter_out_public_procurement(entries):
    return entries.filter(public_procurement=False)
