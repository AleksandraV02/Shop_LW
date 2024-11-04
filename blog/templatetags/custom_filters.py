from django import template
from django.utils.html import strip_tags

register = template.Library()


@register.filter
def strip_html_tags(value):
    return strip_tags(value)


@register.filter
def remove_nbsp(value):
    return value.replace('&nbsp;', '')
