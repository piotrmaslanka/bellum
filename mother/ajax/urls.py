from django.conf.urls.defaults import *

urlpatterns = patterns('bellum.mother.ajax',
                       
    (r'^namechange/$', 'namechange.process'),
    (r'^btools/order/$', 'btools.order'),
    (r'^ttools/order/$', 'ttools.order'),
    (r'^btools/cancel/$', 'btools.cancel'),
    (r'^ttools/cancel/$', 'ttools.cancel'),
    (r'^sendres/$', 'sendres.process'),
    (r'^latools/$', 'latools.order'),
    (r'^relocate/$', 'relocate.process'),   # p is target planet id
)
