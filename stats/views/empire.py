# coding=UTF-8
from djangomako.shortcuts import render_to_response
from django.db.models import Sum
from bellum.common.session.login import must_be_logged
from bellum.common.session import getRace, getAccount, getResourceIndex
from bellum.common.session.mother import getCurrentMother
from bellum.province.models import ProvintionalPresence, Reinforcement
from bellum.common.gui import PrimaryGUIObject
from bellum.common.fixtures.province_build import getCosts
from bellum.alliance.models import Alliance, AllianceMembership
from django.core.exceptions import ObjectDoesNotExist
from bellum.orders.models import TechnologyResearchOrder, MotherConstructionOrder, \
                                 LandarmyProduceOrder, LandarmyProvintionalStrikeOrder, \
                                 LandarmyPlanetaryStrikeOrder, LandarmyMotherPickupOrder, \
                                 ProvinceBuildOrder, ResourceSendOrder
from bellum.common.alliance import isAllied
from bellum.common.utils import humanize__convertSeconds
from bellum.common.fixtures.landarmy_stats import UNIT_NAMES
from bellum.common.fixtures.technology import TECHNOLOGY_NAMES
from bellum.common.fixtures.mother_construction import CONSTRUCTION_NAMES
from bellum.common.fixtures.province_build import BUILDING_NAMES
from bellum.meta import MGID
from django.utils.html import escape
from bellum.stats.models import RankingNone, RankingAlliance
from bellum.common.utils import humanize__designation

@must_be_logged
def process(request):
    mother = getCurrentMother(request)              # The most basic issues
    account = getAccount(request)

    try:                                            # Alliance issues
        alliance = AllianceMembership.objects.get(account=account)
    except ObjectDoesNotExist:
        alliance = None


    presences = ProvintionalPresence.objects.filter(owner=account)  # Get all my provinces

    # Get all build orders on those
    province_builds = ProvinceBuildOrder.objects.filter(ppresence__in=presences)

    planets = []                        # Get raw planets handle, will be useful in counting them
    provinces = []                      # BTW, get province handles.
    for presence in presences:
        if not presence.province.planet in planets: planets.append(presence.province.planet)
        provinces.append(presence.province)
        # Provinces table is needed down there for some freaky shit concerning troops.
        # I'm quite sure those provinces thingy could be fixed by some annotation shit, but it would
        # utterly and terribly confuse me, and affect code readability

                                        # Get researches/builds on my mother
    researches = TechnologyResearchOrder.objects.filter(mother=mother)
    builds = MotherConstructionOrder.objects.filter(mother=mother)
    
                                        # Get troop building queues
    troop_training = LandarmyProduceOrder.objects.filter(mother=mother).order_by('-got__to_be_completed')
                                        # Calculate number of troops in training
    x = troop_training.aggregate(amount=Sum('amount'))['amount']
    if x == None:
        queued_troop_count = 0
    else:
        queued_troop_count = x

                                        # Rock'n'roll here!
                        # Get my outbound salads
    outbound_salad = ResourceSendOrder.objects.filter(send_from=mother)
    inbound_salad = ResourceSendOrder.objects.filter(send_to=mother)
    
    my_outbounds = LandarmyProvintionalStrikeOrder.objects.filter(attacker=account)
        # Select movements TOWARDS MY PROVINCES [supplied by a province list] which are NOT MINE
    inbounds_concerning_me = LandarmyProvintionalStrikeOrder.objects.filter(dstprovince__in=provinces).exclude(attacker=account)
    my_strikes = LandarmyPlanetaryStrikeOrder.objects.filter(mother=mother)
    strikes_concerning_me = LandarmyPlanetaryStrikeOrder.objects.filter(province__in=provinces).exclude(mother__owner=account)
    evacs = LandarmyMotherPickupOrder.objects.filter(mother=mother)
    # Sorry sad statemento follows.
    # This view, by the virtue of it's existence, fucks the database without any contraception.
    # And she will be hurt.

    # I will get back to optimizing this some other time.

    # I promise.
    # TODO: Optimize this view

    allegiance_tab = {}
    for planet in planets:
        for province in planet.province_set.all():
            # 0 - MINE, 1 - ENEMY, 2 - ALLIED, 3 - NOBODYS
            try:
                province.presence
            except:
               allegiance_tab[province.id] = 3
            else:
                # get allegiance
                if province.presence.owner == getAccount(request):
                    allegiance_tab[province.id] = 0
                elif isAllied(getAccount(request), province.presence.owner):
                    allegiance_tab[province.id] = 2
                else:
                    allegiance_tab[province.id] = 1

    if alliance == None:  # alliance is a presence object
        alliance_o = None
    else:
        alliance_o = alliance.alliance # true Alliance object

    try:        # Get alliance ranking
        alliance_ranking = RankingAlliance.objects.get(alliance=alliance_o)
    except:
        alliance_ranking = None

    try:
        player_ranking = RankingNone.objects.get(account=getAccount(request))
    except:
        player_ranking = None
    

    return render_to_response('stats/empire/empire.html',{'pgo':PrimaryGUIObject(request),
                                                          'alliance_m':alliance,
                                                          'alliance_ranking':alliance_ranking,
                                                          'player_ranking':player_ranking,
                                                          'alliance':alliance_o,
                                                          'race':getRace(request),
                                                          'mother':mother,
                                                          'account':account,
                                                          'province_count':presences.count(),
                                                          'planet_count':len(planets),
                                                          'queued_troop_count':queued_troop_count,
                                                          'troop_count':0,
                                                          'troops_training':troop_training,
                                                          'outbound_salad':outbound_salad,
                                                          'inbound_salad':inbound_salad,
                                                          'researches':researches,
                                                          'mother_builds':builds,
                                                          'prov_outbounds':my_outbounds,
                                                          'prov_inbounds':inbounds_concerning_me,
                                                          'prov_builds':province_builds,
                                                          'mother_inbounds':my_strikes,
                                                          'foreign_mother_inbounds':strikes_concerning_me,
                                                          'my_evacs':evacs,
                                                          'mother_name':mother.name,
                                                          'planets':planets,
                                                          'allegiance_tab':allegiance_tab,
                                                          })


def xescape(esc):
    '''redesigned escape so does escape apostrophes properly'''
    esc = esc.replace('\'','\\\'')
    return escape(esc)

                    # global timer object prefix: gto_

def htmlize_salad(salad, mine):     # timer identifier:     sld_<salad.id>
    if mine:
        x = u'<p>Wysyłasz surowce do <b>'+salad.send_to.owner.empire+'</b></p>'
    else:
        x = u'<p>Otrzymujesz surowce od <b>'+salad.send_from.owner.empire+'</b></p>'
    x += u'Tytan: <b>'+str(salad.titan)+'</b><br>'
    x += u'Pluton: <b>'+str(salad.pluton)+'</b><br>'
    x += u'Manpower: <b>'+str(salad.men)+'</b><br>'
    x += u'ETA: <b id=\\\'gto_sld_'+str(salad.id)+'\\\'></b>'
    return x

def htmlize_provbuild(porder):          # pbd_<porder.id>
    x = '<p><b>'+BUILDING_NAMES[porder.what]+'</b> na <b>'+porder.ppresence.province.name+'</b></p>'
    ctype, lvl = porder.ppresence.getPair(porder.slot)
    if ctype == 0:  # wlasnie cos budujemy
        x += u'Budowa <br>'
    else:
        x += u'Rozbudowa na poziom '+str(lvl+1)+'<br>'
    x += u'Pozostało <b id=\\\'gto_pbd_'+str(porder.id)+'\\\'></b>'
    return x

def htmlize_reloc(mother):      # rlc_<mother.id>
    x = u'<p>Relokacja do <b>'+xescape(mother.duePosition().name)+'</b><br>'
    x += u'ETA: <b id=\\\'gto_rlc_'+str(mother.id)+'\\\'></b>'
    return x

def htmlize_produceorder(porder, race):     # lpr_<porder.id>
    x = u'<p><b>'+UNIT_NAMES[race][porder.sold_nr]+'</b><br>'
    x += u'Ilość: <b>'+str(porder.amount)+u'</b><br>';
    x += u'Pozostało: <b id=\\\'gto_lpr_'+str(porder.id)+'\\\'></b>'
    x += '</p>'
    return x

def htmlize_researchorder(rorder):      # rsr_<rorder.id>
    x = '<p><b>' + TECHNOLOGY_NAMES[rorder.what] + '</b> na poziom '+str(rorder.mother.owner.technology.getTechnologyLevelById(rorder.what)+1)+'<br>'
    x += u'Pozostało: <b id=\\\'gto_rsr_'+str(rorder.id)+'\\\'></b>'
    x += '</p>'
    return x

def htmlize_constructorder(ib):     # cst_<ib.id>
    x = '<p><b>' + CONSTRUCTION_NAMES[ib.what] + '</b> na poziom '+str(ib.mother.getConstructionLevelById(ib.what)+1)+'<br>'
    x += u'Pozostało: <b id=\\\'gto_cst_'+str(ib.id)+'\\\'></b>'
    x += '</p>'
    return x

def htmlize_provstrike(ib, display_garrison=False):     # pstr_<ib.id>
    x = '<p><b>'+xescape(ib.srcprovince.planet.name)+'</b><br>'
    x += 'Z: <b>'+xescape(ib.srcprovince.name)+'</b><br>'
    x += 'Do: <b>'+xescape(ib.dstprovince.name)+'</b><br>'
    x += 'Gracz: <b>'+xescape(ib.attacker.empire)+'</b><br>'
    x += 'Desygnata: <b>'+humanize__designation(ib.designation)+'</b><br>'
    x += u'ETA: <b id=\\\'gto_pstr_'+str(ib.id)+'\\\'></b><br>'
    if display_garrison:
        x += 'Garnizon: <p style=\\\'padding-left: 1em;\\\'>'
        for i in xrange(0, MGID+1):
            if ib.garrison[i] > 0:
                x += UNIT_NAMES[ib.attacker.race][i]
                x += ': <b>'+str(ib.garrison[i])+'</b><br>'
        x += '</p>'
    x += '</p>'
    return x

def htmlize_planstrike(ib, display_garrison=False):     # drop_<ib.id>
    x = '<p><b>'+xescape(ib.province.planet.name)+'</b><br>'
    x += 'Z: <b>'+xescape(ib.mother.name)+'</b> [<b>'+escape(ib.mother.owner.empire)+'</b>]<br>'
    x += 'Do: <b>'+xescape(ib.province.name)+'</b><br>'
    x += 'Desygnata: <b>'+humanize__designation(ib.designation)+'</b><br>'
    x += u'ETA: <b id=\\\'gto_drop_'+str(ib.id)+'\\\'></b><br>'
    if display_garrison:
        x += 'Garnizon: <p style=\\\'padding-left: 1em;\\\'>'
        for i in xrange(0, MGID+1):
            if ib.garrison[i] > 0:
                x += UNIT_NAMES[ib.mother.owner.race][i]
                x += ': <b>'+str(ib.garrison[i])+'</b><br>'
        x += '</p>'
    x += '</p>'
    return x

def htmlize_evac(ib):       # evac_<ib.id>
    x = '<p>'
    x += 'Z: <b>'+xescape(ib.province.name)+'</b><br>'
    x += 'Do: <b>'+xescape(ib.mother.name)+'</b><br>'
    x += u'ETA: <b id=\\\'gto_evac_'+str(ib.id)+'\\\'></b><br>'
    x += 'Garnizon: <p style=\\\'padding-left: 1em;\\\'>'
    for i in xrange(0, MGID+1):
        if ib.garrison[i] > 0:
            x += UNIT_NAMES[ib.mother.owner.race][i]
            x += ': <b>'+str(ib.garrison[i])+'</b><br>'
    x += '</p></p>'
    return x
