'''
This module contains common functions used by whole code
'''

from time import mktime
from datetime import datetime
from django import forms

def timestamp__fromDatetime(dt):
    return mktime(dt.timetuple())

def datetime__fromTimestamp(ts):
    return datetime.fromtimestamp(ts)

class DefaultZeroIntegerField(forms.IntegerField):
    '''A Django IntegerField that returns 0 on empty fields'''
    def clean(self, value):
        x = forms.IntegerField.clean(self, value)
        if x == None:
            return 0
        return x
        