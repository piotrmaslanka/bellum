from django.conf.urls.defaults import *

urlpatterns = patterns('bellum.province',
    (r'^ajax/btools/order/$', 'btools.order'),
    (r'^ajax/btools/erect/$', 'btools.erect'),
    (r'^ajax/btools/cancel/$', 'btools.cancel'),
    (r'^ajax/radar/$', 'radar.radar'),
    (r'^ajax/scanner/$', 'radar.scanner'),
)
