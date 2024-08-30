#не совсем понятно для чего таг, внимательно посмотреть когда новостей для сортировки будет много!
from django import template
#from news.models import *
register = template.Library()

@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    d = context['request'].GET.copy()
    for k, v in kwargs.items():
        d[k] = v
    return d.urlencode()
