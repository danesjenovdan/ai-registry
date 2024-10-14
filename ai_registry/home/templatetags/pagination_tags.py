from django import template

register = template.Library()


@register.simple_tag
def query_string_replace(request, **kwargs):
    copied_get = request.GET.copy()
    for k, v in kwargs.items():
        copied_get[k] = v
    return copied_get.urlencode()
