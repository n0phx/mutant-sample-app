# -*- coding: utf-8 -*-
from django import template


register = template.Library()


@register.filter
def get_field_type(field):
    return field.type_cast().__class__.__name__
