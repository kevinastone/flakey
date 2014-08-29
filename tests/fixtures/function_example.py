from django.utils import strip_tags

import django.utils

strip_tags('asdf')

def some_func():
    strip_tags('asdf')

django.utils.strip_tags('assdf')

def another_func():
    django.utils.strip_tags('assdf')
