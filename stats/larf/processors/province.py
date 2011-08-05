# coding=UTF-8
from bellum.stats.larf.const import *
from bellum.stats.larf.processors import ensure
from bellum.register.models import Account
from bellum.province.models import Province
from bellum.common.session import getAccountId
from bellum.stats.larf.const import LX_DROP_COMBAT_LAND, LX_PROVINCE_COMBAT_LAND
from bellum.stats.larf.storage import insertFor
from bellum.common.fixtures.province_build import BUILDING_NAMES
from django.utils.html import escape
LP_LIST = (LP_BUILD_ORDERED, LP_BUILD_CANCELLED,
           LP_DEPLOY_LAND_GROUND, LP_MOTHER_PICKUP_LAND)
           
def dispatch(request, action, *args, **kwargs):
    p = ensure(kwargs['pid'], Province)
    a = getAccountId(request)
    if action == LP_MOTHER_PICKUP_LAND:
        insertFor(a, u'Wysłałeś na matkę garnizon z <a href="/space/planetview/'+unicode(p.planet.id)+'/?province='+unicode(p.id)+'">'+escape(p.name)+u'</a>')
    if action == LP_DEPLOY_LAND_GROUND:
        target = ensure(kwargs['target'], Province)
        insertFor(a, u'Wysłałeś garnizon z <a href="/space/planetview/'+unicode(p.planet.id)+'/?province='+unicode(p.id)+'">'+p.name+u'</a> na <a href="/space/planetview/'+unicode(target.planet.id)+'/?province='+unicode(target.id)+'">'+escape(target.name)+u'</a>')
    if action == LP_BUILD_ORDERED:
        insertFor(a, u'Nakazano rozbudowę <span>'+BUILDING_NAMES[kwargs['what']]+'</span> na <a href="/space/planetview/'+unicode(p.planet.id)+'/?province='+unicode(p.id)+'">'+escape(p.name)+u'</a> na poziom <span>'+unicode(kwargs['levelfrom']+1)+'</span>')
    if action == LP_BUILD_CANCELLED:
        insertFor(a, u'Anulowano rozbudowę <span>'+BUILDING_NAMES[kwargs['what']]+'</span> na <a href="/space/planetview/'+unicode(p.planet.id)+'/?province='+unicode(p.id)+'">'+escape(p.name)+u'</a> na poziom <span>'+unicode(kwargs['levelcurrent']+1)+'</span>')