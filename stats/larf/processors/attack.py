# coding=UTF-8
from bellum.stats.larf.const import *
from bellum.stats.larf.processors import ensure
from bellum.register.models import Account
from bellum.province.models import Province
from bellum.stats.larf.const import LX_DROP_COMBAT_LAND, LX_PROVINCE_COMBAT_LAND
from bellum.stats.larf.storage import insertFor
from django.utils.html import escape
'''request for our dispatcher is totally moot right now'''

LX_LIST = (LX_DROP_COMBAT_LAND, LX_PROVINCE_COMBAT_LAND)

def dispatch(request, action, *args, **kwargs):
    attacker = ensure(kwargs['attacker_id'], Account)
    defender = ensure(kwargs['defender_id'], Account)

    sdict = {True: u'wygrałeś', False:u'przegrałeś', None:u'nastąpił remis'}
    notf = lambda x: {True:False, False:True, None:None}[x]

    if action == LX_DROP_COMBAT_LAND:
        prov = ensure(kwargs['province_id'], Province)
        pp = u'<a href="/space/planetview/'+unicode(prov.planet.id)+'/?province='+unicode(prov.id)+'">'+escape(prov.name)+u'</a>'
        pp = u'Zaatakowałeś '+pp+u' z zrzutu lotniczego i '
        pp = pp + '<span>'+sdict[kwargs['attacker_won']]+'</span>'
        insertFor(attacker.id, pp)
        pp = u'Zostałeś zaatakowany na <a href="/space/planetview/'+unicode(prov.planet.id)+'/?province='+unicode(prov.id)+'">'+escape(prov.name)+u'</a>'
        pp += u' i '+sdict[notf(kwargs['attacker_won'])]
        insertFor(defender.id, pp)
    if action == LX_PROVINCE_COMBAT_LAND:
        prov = ensure(kwargs['target_pid'], Province)
        pp = u'<a href="/space/planetview/'+unicode(prov.planet.id)+'/?province='+unicode(prov.id)+'">'+escape(prov.name)+u'</a>'
        pp = u'Zaatakowałeś '+pp+u' z swojej prowincji i '
        pp = pp + '<span>'+sdict[kwargs['attacker_won']]+'</span>'
        insertFor(attacker.id, pp)
        pp = u'Zostałeś zaatakowany na <a href="/space/planetview/'+unicode(prov.planet.id)+'/?province='+unicode(prov.id)+'">'+escape(prov.name)+u'</a>'
        pp += u' i <span>'+sdict[notf(kwargs['attacker_won'])]+'</span>'
        insertFor(defender.id, pp)
