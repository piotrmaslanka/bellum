# coding=UTF-8
from bellum.stats.larf.const import *
from bellum.alliance.models import Alliance
from bellum.register.models import Account
from bellum.stats.larf.storage import insertFor
from bellum.stats.larf.processors import ensure, ensureID
from django.utils.html import escape

LA_LIST = (LA_DISBAND_ALLIANCE, LA_CREATE_ALLIANCE,
           LA_LEAVE_ALLIANCE, LA_APPLIED_TO_ALLIANCE,
           LA_DECLINED_APPLICATION_TO_ALLIANCE,
           LA_ACCEPTED_APPLICATION_TO_ALLIANCE,
           LA_KICKED_FROM_ALLIANCE, LA_MODIFIED_TEAMSITE,
           LA_MADE_LEADER, LA_ALLIANCE_BROADCAST)

def dispatch(request, action, *args, **kwargs):
    alliance = ensure(kwargs['aid'], Alliance)
    if action == LA_DISBAND_ALLIANCE:
        for mmbr in alliance.alliancemembership_set.all():
            insertFor(mmbr.account.id, u'Sojusz <span>'+escape(mmbr.alliance.name)+u'</span> został rozwiązany')
    if action == LA_LEAVE_ALLIANCE:
        insertFor(ensureID(kwargs['accid']), u'Opuściłeś sojusz')
    if action == LA_MADE_LEADER:
        insertFor(ensureID(kwargs['newleader']), u'Zostałeś liderem sojuszu')
        newldr = ensure(kwargs['newleader'], Account)
        insertFor(ensureID(kwargs['oldleader']), u'Przekazałeś pozycję lidera graczowi <a href="/uprofile/view/'+unicode(newldr.id)+'">'+escape(newldr.empire)+'</a>')

