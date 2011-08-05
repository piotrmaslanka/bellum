from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^(?P<path>.*)$', 'bellum.portal.process'),
)

