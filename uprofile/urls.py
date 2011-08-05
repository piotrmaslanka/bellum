from django.conf.urls.defaults import *

urlpatterns = patterns('bellum.uprofile.views',
                       
    (r'^edit/$', 'edit.process'),
    (r'^edit/password/$', 'edit.process', {'do_password':True}),
    (r'^edit/avatar/$', 'edit.process', {'do_avatar':True}),
    (r'^view/(?P<acc_id>\d+)/$', 'view.process'),

)
