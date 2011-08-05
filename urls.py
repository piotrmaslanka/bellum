from django.conf.urls.defaults import *

urlpatterns = patterns('',
                       
    (r'^alliance/', include('bellum.alliance.urls')),
    (r'^mother/', include('bellum.mother.urls')),
    (r'^register/', include('bellum.register.urls')),
    (r'^uprofile/', include('bellum.uprofile.urls')),
    (r'^province/', include('bellum.province.urls')),
    (r'^space/', include('bellum.space.urls')),
    (r'^chat/', include('bellum.chat.urls')),
    (r'^stats/', include('bellum.stats.urls')),
    (r'^portal/', include('bellum.portal.urls')),
    (r'^robots.txt', 'bellum.robots'),
    (r'^$', 'bellum.register.views.login.process'),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': 'D:/projects/webapps/bellum/media',
        })

)
