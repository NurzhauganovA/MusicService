from django import template

register = template.Library()


@register.filter(name='split')
def split(value, splitter):
    return value.split(splitter)
