from django.conf.urls.defaults import *

urlpatterns = patterns('bellum.mother.views',

    (r'^ajax/', include('bellum.mother.ajax.urls')),
    (r'^overview/$', 'overview.process'),
    (r'^garrison/land/$','garrison.land'),
)
