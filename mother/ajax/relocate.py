# coding=UTF-8
'''Handles relocation issues'''
from django.shortcuts import redirect
from djangomako.shortcuts import render_to_response
from bellum.common.session.login import must_be_logged_ajax
from django.http import HttpResponse
from bellum.common.session.mother import getCurrentMother
from bellum.common.session import getAccount
from bellum.space.models import Planet
from bellum.orders.mother.relocate import orderRelocate
from bellum.common.session import getRace
from bellum.stats.larf import note
from bellum.stats.larf.const import LM_RELOCATION

@must_be_logged_ajax
def process(request):
    '''Handles issues connected to mothership relocation
    Is a frontend to issuing a relocation order
    May also display that a relocation is in progress'''
    mum = getCurrentMother(request)

    try:
        target = Planet.objects.get(id=int(request.GET['p']))
    except:
        return HttpResponse('ERROR')

    if not mum.canRelocate(): return HttpResponse('ERROR')
    
    orderRelocate(mum, getRace(request), target)
    note(request, LM_RELOCATION, mid=mum.id,
                                 source=mum.orbiting.id,
                                 target=target)
    return HttpResponse('OK')