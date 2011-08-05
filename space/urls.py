from django.conf.urls.defaults import *

urlpatterns = patterns('bellum.space.views',

    (r'^regionmap/(?P<planet_id>\d+)/$', 'regionmap.from_planet'),
    (r'^regionmap/$', 'regionmap.from_mother'),
    (r'^regionmap/(?P<x>[0-9\-]+)/(?P<y>[0-9\-]+)/$', 'regionmap.from_coords'),

    (r'^planetview/(?P<planet_id>\d+)/$', 'planetview.process'),
    (r'^planetview/province/(?P<province_id>\d+)/$', 'planetview.process_onlyprovince'),
    (r'^troopmove/(?P<province_id>\d+)/$', 'troopmove.dxprovince'),
    (r'^troopmove/mother/$', 'troopmove.dxmother'),
    (r'^troopmove/submit/$', 'troopmove.submit'),
    (r'^troopmove/cancel/drop/$', 'troopmove.cancel_drop'),
    (r'^troopmove/cancel/strike/$', 'troopmove.cancel_strike'),
    (r'^ajax/', include('bellum.space.ajax.urls')),
)
