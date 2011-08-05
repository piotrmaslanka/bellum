# coding=UTF-8
'''Suite of AJAX tools to do with Mothership constructions'''
from django.http import HttpResponse
from bellum.common.session.login import must_be_logged_ajax
from bellum.common.session.mother import getCurrentMother
from bellum.common.session import getResourceIndex, getRace, getAccount
from bellum.orders.models import GenericOrderTable, MotherConstructionOrder
from bellum.common.fixtures.mother_construction import getCosts, getRequirements
from datetime import datetime
from time import mktime, time
from bellum.orders.mother.construct import orderConstruct, cancelConstruct
from bellum.stats.larf import note
from bellum.stats.larf.const import LM_CONSTRUCTION_ORDERED, LM_CONSTRUCTION_CANCELLED

from bellum.meta import MBI

def what_available(proc):
    def what_available_decorator(*args, **kwargs):
        try:
            if not (int(args[0].GET['what']) in range(0, MBI+1)):
                raise Exception
        except:
            return HttpResponse('/')
        return proc(*args, **kwargs)
    return what_available_decorator

@must_be_logged_ajax
@what_available
def cancel(request):
    '''Cancels a construction.
            Doable: Always
            Profits: Nothing'''
    mum = getCurrentMother(request)
    
    try:
        tek, = MotherConstructionOrder.objects.filter(mother=mum).filter(what=int(request.GET['what']))
    except ValueError:
        return HttpResponse('NONE')
   
    try:
        cancelConstruct(tek)

        note(request, LM_CONSTRUCTION_CANCELLED, mid=mum.id,
                                                 what=int(request.GET['what']),
                                                 levelcurrent=mum.__dict__['b_'+request.GET['what']])
    except:
        return HttpResponse('LOL-ERROR')
    return HttpResponse('OK')

@must_be_logged_ajax
@what_available
def order(request):    
    mum = getCurrentMother(request)
    
    costs = getCosts(mum, getRace(request), int(request.GET['what'])) 
    
    if costs[0] > getResourceIndex(request).stateUpdate():
        return HttpResponse('COSTS')
    if mum.getPendingConstructionsCount() > 0:
        return HttpResponse('QUEUE')
    if not getRequirements(mum, getRace(request), int(request.GET['what'])).validate(mum):
        return HttpResponse('REQUIREMENTS')   

    note(request, LM_CONSTRUCTION_ORDERED, mid=mum.id,
                                           what=int(request.GET['what']),
                                           levelfrom=mum.__dict__['b_'+request.GET['what']])
    
    orderConstruct(mum, int(request.GET['what']), costs)
    return HttpResponse('OK')
    
