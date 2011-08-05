# coding=UTF-8
from django.shortcuts import redirect
from bellum.common.alliance import isAllied
from bellum.common.session.login import must_be_logged
from bellum.common.session import getAccount, getRace
from bellum.common.session.mother import getCurrentMother
from djangomako.shortcuts import render_to_response, render_to_string
from bellum.space.models import Planet
from bellum.common.gui import PrimaryGUIObject
from bellum.common.fixtures.province_build import getCosts
from bellum.common.session import getRace, getAccount, getResourceIndex
from bellum.meta import MPBI
from bellum.province.models import Province, Reinforcement
from django.core.exceptions import ObjectDoesNotExist
from bellum.orders.models import LandarmyProvintionalStrikeOrder
from bellum.orders.models import LandarmyPlanetaryStrikeOrder, LandarmyProvintionalStrikeOrder, LandarmyMotherPickupOrder
from bellum.space.ajax.pinfo import dx_html
from bellum.common.fixtures.relocation import getRelocationTime

@must_be_logged
def process_onlyprovince(request, province_id):
    try:    # check planet
        province_id = int(province_id)
        province = Province.objects.get(id=province_id)
    except:
        return redirect('/')
    return process(request, province.planet.id, province_id=province_id)

@must_be_logged
def process(request, planet_id, province_id=None):
    try:    # check planet
        planet = Planet.objects.get(id=planet_id)
    except:
        return redirect('/')

    provinces = Province.objects.filter(planet=planet)
    provinces_postprocessed = {}
    prov = None

    try:    # faciliates GET getting province to zoom onto
        if province_id != None:
            provgrabber = province_id
        else:
            provgrabber = int(request.GET['province'])
    except:
        provgrabber = None

    for province in provinces:
            # 0 - MINE, 1 - ENEMY, 2 - ALLIED, 3 - NOBODYS
        try:
            province.provintionalpresence
        except:
            pv = 'gray'
        else:
            if province.provintionalpresence.owner == getAccount(request):
                pv = 'green'
            elif isAllied(getAccount(request), province.provintionalpresence.owner):
                pv = 'blue'
            else:
                pv = 'red'

        provinces_postprocessed[province.id] = [pv, False]

        if province.id == provgrabber:
            prov = province

        try:
            if province.provintionalpresence.owner == getAccount(request):
                if prov == None:
                       prov = province
        except:
            pass

    if prov == None:
        prov = provinces[0]

    provinces_postprocessed[prov.id][1] = True
    mum = getCurrentMother(request)

    sfx = dx_html(request, prov, mum).decode('utf8')

    # can relocate?
    can_relocate = False
    relocation_time = None
    if (planet != mum.duePosition()):   # Different position than current
        can_relocate = mum.canRelocate()
        if can_relocate:
            relocation_time = getRelocationTime(mum, getRace(request), mum.orbiting, planet)

    # can scan?
    can_scan = False
    if getRace(request) == 1:
        if mum.isRelocating() == False:
            if mum.orbiting == planet:
                can_scan = True
        

    return render_to_response('space/planetview/planetview.html', {'htmldata':sfx,
                                                                   'race':getRace(request),
                                                                   'planet':planet,
                                                                   'postprocessed':provinces_postprocessed,
                                                                   'can_scan':can_scan,
                                                                   'firstprovince':prov,
                                                                   'can_relocate':can_relocate,
                                                                   'relocation_time':relocation_time,
                                                                   'wctg':lambda x: int((x+100.0)*(345.0/200.0)),
                                                                   'pgo':PrimaryGUIObject(request)})
