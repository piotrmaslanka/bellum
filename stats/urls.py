from django.conf.urls.defaults import *

urlpatterns = patterns('bellum.stats.views',
                       
    (r'^income/', 'income.process'),
    (r'^larf/', 'larf.process'),
    (r'^empire/', 'empire.process'),

    (r'^ranking/all/$', 'ranking.process', {'rankingtype':'all', 'page':1}),
    (r'^ranking/all/me/$', 'ranking.process', {'rankingtype':'all', 'page':None}),
    (r'^ranking/all/(?P<page>\d+)/$', 'ranking.process', {'rankingtype':'all'}),

    (r'^ranking/mother/$', 'ranking.process', {'rankingtype':'mother', 'page':1}),
    (r'^ranking/mother/me/$', 'ranking.process', {'rankingtype':'mother', 'page':None}),
    (r'^ranking/mother/(?P<page>\d+)/$', 'ranking.process', {'rankingtype':'mother'}),

    (r'^ranking/army/$', 'ranking.process', {'rankingtype':'army', 'page':1}),
    (r'^ranking/army/me/$', 'ranking.process', {'rankingtype':'army', 'page':None}),
    (r'^ranking/army/(?P<page>\d+)/$', 'ranking.process', {'rankingtype':'army'}),

    (r'^ranking/allied/$', 'ranking.process', {'rankingtype':'allied', 'page':1}),
    (r'^ranking/allied/me/$', 'ranking.process', {'rankingtype':'allied', 'page':None}),
    (r'^ranking/allied/(?P<page>\d+)/$', 'ranking.process', {'rankingtype':'allied'}),
)
