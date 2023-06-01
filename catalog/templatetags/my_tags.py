import datetime
from django import template

register = template.Library()


@register.simple_tag
def current_year():
    return datetime.datetime.now().strftime('%Y')


@register.simple_tag
def mediapath(path_from_object):
    return path_from_object.url


@register.filter
def mediapath(path_from_object):
    return path_from_object.url

