from bellum.province import pp_available, p_available
from bellum.mother.models import Mother
from bellum.orders.models import MotherRelocationOrder
from bellum.common.session.login import must_be_logged_ajax
from django.http import HttpResponse
from bellum.stats.reports import makeReport, sendTo
from bellum.common.session import getAccount
from django.shortcuts import redirect
from bellum.common.session.login import must_be_logged
from bellum.common.session.mother import getCurrentMother
from bellum.common.session import getAccount
from datetime import datetime
from bellum.orders.models import MotherRelocationOrder, LandarmyMotherPickupOrder, LandarmyPlanetaryStrikeOrder
from bellum.space.models import Planet
from bellum.province.models import Province
from bellum.orders.mother.relocate import orderRelocate
from django import forms
from bellum.common.utils import datetime__secondsToNow
from bellum.common.session import getRace
from bellum.stats.larf import note
from bellum.orders.mother.scan import doScan
from bellum.province.models import Province

@must_be_logged_ajax
@p_available
def scanner(request, p):
    '''Scans a target province in GET 'p' '''
    mum = getCurrentMother(request)
    acc = getAccount(request)

    if getRace(request) != 1: return HttpResponse('RACE')
    if mum.isRelocating(): return HttpResponse('RELOCATION')
    if not p in mum.orbiting.province_set.all(): return HttpResponse('PROVINCE')

    doScan(acc, mum, p)

    return HttpResponse('OK')

@must_be_logged_ajax
@pp_available
def radar(request, pp):
    '''needs a presence in 'pp' '''
    if pp.owner != getAccount(request): return HttpResponse('ACCOUNT')

    radarlevel = 0
    for i in xrange(0, pp.province.slots):
        otype, olvl = pp.getPair(i)
        if otype == 4:
            if olvl > radarlevel: radarlevel = olvl

    if radarlevel == 0: return HttpResponse('NORADAR')

    ms = Mother.objects.filter(orbiting=pp.province.planet)
    mros_i = MotherRelocationOrder.objects.filter(loc_to=pp.province.planet)
    mros_o = MotherRelocationOrder.objects.filter(loc_from=pp.province.planet)

    sms = filter(lambda x: (not x in mros_i) and (not x in mros_o), ms)

    srl = RadarReportv01(pp.province, radarlevel)

    if radarlevel >= 1:   # radar lv 1
        for mum in sms:
            srl.appendStationary(mum)
    if radarlevel >= 2:   # radar lv 2
        for mum in mros_i:
            srl.appendInbound(mum)
    if radarlevel >= 3:   # radar lv 3
        for mum in mros_o:
            srl.appendOutbound(mum)

    rp = makeReport(srl)
    sendTo(rp, getAccount(request), u'Raport radaru z '+pp.province.name)

    return HttpResponse('OK')
