from djangomako.shortcuts import render_to_string
from bellum.common.session.login import must_be_logged
from bellum.common.session import getAccount, getRace
from bellum.common.gui import PrimaryGUIObject
from bellum.province.models import Province, Reinforcement
from bellum.common.session.mother import getCurrentMother
from bellum.common.fixtures.province_build import getCosts
from bellum.meta import MPBI
from django.core.exceptions import ObjectDoesNotExist
from bellum.space.ajax import p_available
from bellum.orders.models import LandarmyProvintionalStrikeOrder
from bellum.orders.models import LandarmyPlanetaryStrikeOrder, LandarmyProvintionalStrikeOrder, LandarmyMotherPickupOrder
from django.http import HttpResponse

def dx_html(request, prov, mum=None):

    ## Uh, take a note that this still needs to limit displaying provinces we don't have a ship at
    if mum == None:
        mum = getCurrentMother(request)

    mother_evacs = LandarmyMotherPickupOrder.objects.filter(province=prov).filter(mother__owner=getAccount(request))
    outgoing_units = LandarmyProvintionalStrikeOrder.objects.filter(srcprovince=prov)


    try:
        prov.presence
    except ObjectDoesNotExist:
            # MY drops incoming at THIS province
        mother_drops = LandarmyPlanetaryStrikeOrder.objects.filter(province=prov).filter(mother__owner=getAccount(request))
            # MY attacks INCOMING at THIS province
        prov_target = LandarmyProvintionalStrikeOrder.objects.filter(dstprovince=prov).filter(attacker=getAccount(request))

        return render_to_string('space/planetview/generator/unclaimed.html',{'pgo':PrimaryGUIObject(request),
                                                                             'my_land_inbound':prov_target,
                                                                             'my_drop_inbound':mother_drops,
                                                                             'province':prov,
                                                                             'race':getRace(request)})

    if prov.presence.owner != getAccount(request):
            # MY drops incoming at THIS province
        mother_drops = LandarmyPlanetaryStrikeOrder.objects.filter(province=prov).filter(mother__owner=getAccount(request))
            # MY moves INCOMING at THIS province
        prov_target = LandarmyProvintionalStrikeOrder.objects.filter(dstprovince=prov).filter(attacker=getAccount(request))
        try:
            reif = Reinforcement.objects.filter(owner=getAccount(request)).get(presence=prov.presence)
        except:
            return render_to_string('space/planetview/generator/public.html',{'pgo':PrimaryGUIObject(request),
                                                                       'my_land_inbound':prov_target,
                                                                       'my_drop_inbound':mother_drops,
                                                                       'race':getRace(request),
                                                                       'province':prov})
        else:
            return render_to_string('space/planetview/generator/reinforcer.html',{'pgo':PrimaryGUIObject(request),
                                                                       'reinforcement':reif,
                                                                       'my_land_inbound':prov_target,
                                                                       'my_drop_inbound':mother_drops,
                                                                       'province':prov,
                                                                       'race':getRace(request)})


    pbs = prov.presence.getPendingBuilds()
    d = {}
    for b in pbs:
        d[b.slot] = b

    firstclear = None
    costs = {}

    for i in xrange(0, prov.slots):
        otype, olvl = prov.presence.getPair(i)
        if otype == 0:
            if firstclear == None:
                firstclear = i
        else:
            costs[i] = getCosts(prov.presence, getRace(request), olvl, otype)

    gcosts = {}
    canerect = {}
    for i in xrange(1, MPBI+1):
        gcosts[i] = getCosts(prov.presence, getRace(request), 0, i)
        canerect[i] = True

    canerect[1] = (prov.titan_coef > 0)
    canerect[2] = (prov.pluton_coef > 0)
    canerect[3] = (prov.town_coef > 0)

        # ANY drops incoming at THIS province
    drops = LandarmyPlanetaryStrikeOrder.objects.filter(province=prov)
        # MY moves INCOMING at THIS province
    prov_target = LandarmyProvintionalStrikeOrder.objects.filter(dstprovince=prov)
        # MY moves OUTBOUND from THIS province
    outgoing_units = LandarmyProvintionalStrikeOrder.objects.filter(srcprovince=prov)
        # MY evacuations from THIS province
    evacs = LandarmyMotherPickupOrder.objects.filter(province=prov)
    return render_to_string('space/planetview/generator/private.html',{'pgo':PrimaryGUIObject(request),
                                                            'race':getRace(request),
                                                            'costs':costs,
                                                            'gcosts':gcosts,
                                                            'land_inbound':prov_target,
                                                            'drop_inbound':drops,
                                                            'evacs_bound':evacs,
                                                            'land_outbound':outgoing_units,
                                                            'province':prov,
                                                            'builds':d,
                                                            'canerect':canerect,
                                                            'account':getAccount(request),
                                                            'first_slot_clear':firstclear})

@must_be_logged
@p_available
def html(request, prov):
    '''This is a direct interface for AJAX access, and needs to be shielded with decorators,
       which tend to totally fuck normal invocations. We need previous function, as it is consumed by
       bellum.space.views.planetview and unencumbered with that crap'''
    s = dx_html(request, prov).decode('utf8')
    return HttpResponse(s)