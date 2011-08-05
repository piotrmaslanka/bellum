from django.conf.urls.defaults import *

urlpatterns = patterns('bellum.space.ajax',

    (r'^pinfo/html/$', 'pinfo.html'), # GET: p is province id
    (r'^tdinfo/planetpick/(?P<planet_id>\d+)/$', 'tdinfo.planetpick_planet'),
    (r'^tdinfo/provincepick/$', 'tdinfo.provincepick'),
    (r'^tdinfo/planetpick/mothership/$', 'tdinfo.planetpick_mother'),

    (r'^regionmap/sector/$', 'regionmap.sector_map'),
    (r'^regionmap/region/$', 'regionmap.region_map'),
    (r'^regionmap/galaxy/$', 'regionmap.galaxy_map'),
)

