import os
import sys

sys.path = ['D:/projects/webapps/'] + sys.path
from django.core.handlers.wsgi import WSGIHandler

os.environ['DJANGO_SETTINGS_MODULE'] = 'bellum.settings'
application = WSGIHandler()