# coding=UTF-8
'''Suite of AJAX tools to do with Province constructions'''
from django.http import HttpResponse
from bellum.common.session.login import must_be_logged_ajax
from bellum.common.session import getAccount, getResourceIndex, getRace
from bellum.common.session.mother import getCurrentMother
from bellum.common.fixtures.province_build import getCosts
from bellum.province.models import ProvintionalPresence
from json import dump
from datetime import datetime
from time import mktime, time
from bellum.orders.province.build import orderBuild, cancelBuild
from bellum.stats.larf import note
from bellum.common.fixtures.province_build import BUILDING_NAMES
from bellum.stats.larf.const import LP_BUILD_ORDERED, LP_BUILD_CANCELLED
from bellum.province import pp_available

@must_be_logged_ajax
@pp_available
def cancel(request, pp):
    slot = int(request.GET['slot'])
    if pp.owner != getAccount(request):
        return HttpResponse('ACCOUNT')

    otype, olvl = pp.getPair(slot)  # if we are cancelling an erection, otype == 0 ...
    try:
        otype = cancelBuild(pp, slot)       # ... therefore this
    except:
        return HttpResponse('UNEXISTANT')

    note(request, LP_BUILD_CANCELLED, what=otype,
                                      pid=pp.province.id,
                                      levelcurrent=olvl)

    return HttpResponse('OK')   
    

@must_be_logged_ajax
@pp_available
def order(request, pp):
    mum = getCurrentMother(request)
    slot = int(request.GET['slot'])

    otype, olvl = pp.getPair(slot)

    if otype == 0:
        return HttpResponse('ZEROSLOT')     # Cannot upgrade something that doesnt exist

    costs = getCosts(pp, getRace(request), olvl, otype)
    
    if pp.owner != getAccount(request):
        return HttpResponse('ACCOUNT')
    if costs[0] > getResourceIndex(request).stateUpdate():
        return HttpResponse('COSTS')
    if pp.getPendingBuildingsCount() > 0:
        return HttpResponse('QUEUE')

    note(request, LP_BUILD_ORDERED, pid=pp.province.id,
                                    slot=slot,
                                    what=otype,
                                    levelfrom=olvl)
    
    orderBuild(pp, mum, otype, slot, costs)
    return HttpResponse('OK')
    
@must_be_logged_ajax
@pp_available
def erect(request, pp):  
    mum = getCurrentMother(request)

    slot = None
    for i in xrange(0, pp.province.slots):
        if pp.getPair(i)[0] == 0:
            slot = i
            break
    if slot == None:
        return HttpResponse('NOFREESLOTS')

    what = int(request.GET['what'])

    otype, olvl = pp.getPair(slot)

    if otype != 0:
        return HttpResponse('NONZEROSLOT') # Can't build in occupied space

    costs = getCosts(pp, getRace(request), 0, what)

    if pp.owner != getAccount(request):
        return HttpResponse('ACCOUNT')
    if costs[0] > getResourceIndex(request).stateUpdate():
        return HttpResponse('COSTS')
    if pp.getPendingBuildingsCount() > 0:
        return HttpResponse('QUEUE')

    if (otype == 1) and (pp.province.titan_coef == 0):
        return HttpResponse('RSFAIL_TITAN')
    if (otype == 2) and (pp.province.pluton_coef == 0):
        return HttpResponse('RSFAIL_TITAN')
    if (otype == 3) and (pp.province.town_coef == 0):
        return HttpResponse('RSFAIL_TITAN')

    note(request, LP_BUILD_ORDERED, pid=pp.province.id,
                                    slot=slot,
                                    what=what,
                                    levelfrom=olvl)

    orderBuild(pp, mum, what, slot, costs)
    return HttpResponse('OK')
