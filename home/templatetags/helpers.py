from decimal import Decimal
from django.template.defaulttags import register
from django.utils import translation



import copy, random, os, hashlib
from PIL import Image

from wagtail.wagtailcore.blocks import StreamValue



@register.filter
def preview(text):
    return text[0:247] + '...' if len(text) >= 250 else text