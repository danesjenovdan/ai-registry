from django import template

register = template.Library()


@register.simple_tag
def query_string_replace(request, **kwargs):
    copied_get = request.GET.copy()
    for k, v in kwargs.items():
        if v is None and k in copied_get:
            del copied_get[k]
        else:
            copied_get[k] = v
    return copied_get.urlencode()
