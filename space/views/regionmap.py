# coding=UTF-8
from django.shortcuts import redirect
from bellum.common.session.login import must_be_logged
from bellum.common.session import getAccount
from bellum.common.session.mother import getCurrentMother
from djangomako.shortcuts import render_to_response
from bellum.space.models import Planet
from bellum.province.models import ProvintionalPresence
from bellum.mother.models import Mother
from bellum.common.gui import PrimaryGUIObject
from django.db.models import Q
from bellum.space.ajax.regionmap import p_secm, p_regm

@must_be_logged
def process(request, x, y):
    '''@x int
       @y int'''
    # Uh, oh, now get neighbouring planets plz
    mpos = getCurrentMother(request).duePosition()
    return render_to_response('space/regionmap/base.html',   {'x':x,
                                                              'y':y,
                                                              'mx':mpos.x,
                                                              'my':mpos.y,
                                                              'fillin_map_content':p_secm(request, x, y).decode('utf8'),
                                                              'pgo':PrimaryGUIObject(request)})

@must_be_logged
def from_planet(request, planet_id):
    try:
        planet = Planet.objects.get(id=planet_id)
    except:
        return redirect('/')

    return process(request, planet.x, planet.y)
    

@must_be_logged
def from_mother(request):
    mother = getCurrentMother(request)
    pos = mother.duePosition()
    return process(request, pos.x, pos.y)

@must_be_logged
def from_coords(request, x, y):
    return process(request, int(x), int(y))