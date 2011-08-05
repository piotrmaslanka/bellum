# coding=UTF-8
from bellum.stats.larf.const import *
from bellum.stats.larf.storage import insertFor
from bellum.stats.larf.processors import ensure, ensureID
from bellum.common.session import getAccountId, getRace
from bellum.province.models import Province
from bellum.mother.models import Mother
from bellum.space.models import Planet
from bellum.common.fixtures.landarmy_stats import UNIT_NAMES
from bellum.common.fixtures.mother_construction import CONSTRUCTION_NAMES
from bellum.common.fixtures.technology import TECHNOLOGY_NAMES
from django.utils.html import escape
LM_LIST = (LM_CONSTRUCTION_ORDERED, LM_CONSTRUCTION_CANCELLED,
           LM_LANDARMY_TRAINING, LM_NAMECHANGE,
           LM_RESEARCH_ORDERED, LM_RESEARCH_CANCELLED,
           LM_DEPLOY_LAND_GROUND, LM_SENT_RESOURCE,
           LM_RELOCATION, LM_RCVD_RESOURCE)

def dispatch(request, action, *args, **kwargs):
    try:
        cacid = getAccountId(request)
    except:
        pass
    if action == LM_DEPLOY_LAND_GROUND:
        p = ensure(kwargs['provinceid'], Province)
        insertFor(cacid, u'Wysłano na <a href="/space/planetview/'+unicode(p.planet.id)+'/?province='+unicode(p.id)+'">'+p.name+u'</a> wojsko')
    if action == LM_RESEARCH_ORDERED:
        insertFor(cacid, u'Nakazano rozwój <span>'+TECHNOLOGY_NAMES[kwargs['what']]+u'</span> na poziom <span>'+unicode(kwargs['levelfrom']+1)+'</span>')
    if action == LM_RESEARCH_CANCELLED:
        insertFor(cacid, u'Anulowano rozwój <span>'+TECHNOLOGY_NAMES[kwargs['what']]+u'</span> na poziom <span>'+unicode(kwargs['levelcurrent']+1)+'</span>')
    if action == LM_CONSTRUCTION_ORDERED:
        insertFor(cacid, u'Nakazano rozbudowę <span>'+CONSTRUCTION_NAMES[kwargs['what']]+u'</span> na poziom <span>'+unicode(kwargs['levelfrom']+1)+'</span>')
    if action == LM_CONSTRUCTION_CANCELLED:
        insertFor(cacid, u'Anulowano rozbudowę <span>'+CONSTRUCTION_NAMES[kwargs['what']]+u'</span> na poziom <span>'+unicode(kwargs['levelcurrent']+1)+'</span>')
    if action == LM_LANDARMY_TRAINING:
        insertFor(cacid, u'Rozpoczęto szkolenie <span>'+unicode(kwargs['amount'])+u'</span> jednostek <span>'+UNIT_NAMES[getRace(request)][kwargs['what']]+'</span>')
    if action == LM_RELOCATION:
        pl = ensure(kwargs['target'], Planet)
        insertFor(cacid, u'Wykonano skok nadprzestrzenny w kierunku <a href="/space/planetview/'+unicode(pl.id)+u'/">'+pl.name+u'</a>')
    if action == LM_SENT_RESOURCE:
        tplayer = ensure(kwargs['target'], Mother).owner
        rs = kwargs['resources']
        insertFor(cacid, u'Wysłałeś <span>'+unicode(rs.titan)+u'</span> tytanu <span>'+unicode(rs.pluton)+u'</span> plutonu <span>'+unicode(rs.men)+u'</span> ludzi do <a href="/uprofile/view/'+unicode(tplayer.id)+'">'+escape(tplayer.empire)+'</a>')
    if action == LM_RCVD_RESOURCE:
        fplayer = ensure(kwargs['mfrom'], Mother).owner
        target = ensure(kwargs['target'], Mother).owner
        rs = kwargs['resources']
        insertFor(target.id, u'Otrzymałeś <span>'+unicode(rs.titan)+u'</span> tytanu <span>'+unicode(rs.pluton)+u'</span> plutonu <span>'+unicode(rs.men)+u'</span> ludzi od <a href="/uprofile/view/'+unicode(fplayer.id)+'">'+escape(fplayer.empire)+'</a>')

