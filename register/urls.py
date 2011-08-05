from django.conf.urls.defaults import *

urlpatterns = patterns('bellum.register.views',
    (r'^activate/$', 'activate.process'),
    (r'^register/$', 'register.process'),
    (r'^login/$', 'login.process'),
    (r'^logout/$', 'logout.process'),
    (r'^passremind/activate/$', 'passremind.activate'),
    (r'^passremind/$', 'passremind.process'),
)