from django.conf.urls.defaults import *

urlpatterns = patterns('bellum.alliance.views',
    (r'^new/$', 'new.process'),
    (r'^view/own/$', 'view.own'),
    (r'^view/(?P<alliance_id>\d+)/$', 'view.other'),
    (r'^members/$', 'members.process'),
    (r'^disband/$', 'disband.process'), # ajaxoid
    (r'^leave/$', 'leave.process'),     # ajaxoid
    (r'^kick/(?P<target_membership_id>\d+)/$', 'kick.process'), # ajaxoid
    (r'^privileges/(?P<target_membership_id>\d+)/toggle/(?P<priv_id>\d+)/$', 'privileges.toggle'),
    (r'^privileges/(?P<target_membership_id>\d+)/rank/$', 'privileges.rank'),   # ajaxoid, GET:rank
    (r'^accept/list/$', 'accept.list'),
    (r'^accept/approve/(?P<application_id>\d+)/', 'accept.approve'),    # redirectoid
    (r'^accept/decline/(?P<application_id>\d+)/', 'accept.decline'),    # redirectoid
    (r'^apply/(?P<alliance_id>\d+)/', 'apply.process'),
    (r'^apply/cancel/', 'apply.cancel'),
    (r'^teamsite/$', 'teamsite.process'),
    (r'^teamsite/avatar/$', 'teamsite.process', {'do_avatar':True}),

    (r'^makeleader/(?P<target_membership_id>\d+)/$', 'makeleader.process'),
)
