# coding=UTF-8
'''Suite of AJAX tools to do with Research'''
from django.http import HttpResponse
from bellum.common.session.login import must_be_logged_ajax
from bellum.common.session import getAccount, getResourceIndex, getRace
from bellum.common.session.mother import getCurrentMother
from bellum.orders.models import GenericOrderTable, TechnologyResearchOrder
from bellum.common.fixtures.technology import getCosts, getRequirements, canAdvance
from datetime import datetime
from time import mktime, time
from bellum.orders.mother.research import orderResearch, cancelResearch
from bellum.stats.larf import note
from bellum.stats.larf.const import LM_RESEARCH_ORDERED, LM_RESEARCH_CANCELLED

from bellum.meta import MTI

def what_available(proc):
    def what_available_decorator(*args, **kwargs):
        try:
            if not (int(args[0].GET['what']) in range(0, MTI+1)):
                raise Exception
        except:
            return HttpResponse('/')
        return proc(*args, **kwargs)
    return what_available_decorator

    
@must_be_logged_ajax
@what_available
def cancel(request):
    '''Cancels a technology research.
            When: Always doable
            Profits: Nothing'''
    mum = getCurrentMother(request)
    
    try:
        tek, = TechnologyResearchOrder.objects.filter(mother=mum).filter(what=int(request.GET['what']))
    except ValueError:
        return HttpResponse('NONE')

    
    try:
        cancelResearch(tek)
        note(request, LM_RESEARCH_CANCELLED, mid=mum.id,
                                             what=int(request.GET['what']),
                                             levelcurrent=mum.owner.technology.__dict__['o_'+request.GET['what']])
    except:
        return HttpResponse('LOL-ERROR')
    return HttpResponse('OK')
    
@must_be_logged_ajax
@what_available
def order(request):
    '''Starts a technology research.
            When:
                    Resources met
                    Not researching any other technology worldwide
                    Requirements met'''
                    
    mum = getCurrentMother(request)
    
    costs = getCosts(mum.owner.technology, getRace(request), int(request.GET['what'])) 
    
    if costs[0] > getResourceIndex(request).stateUpdate():
        return HttpResponse('COSTS')

    if int(request.GET['what']) == 12:            # supercomputer
        if getAccount(request).getPendingResearchesCount() > 0:
            return HttpResponse('QUEUE')
    else:
        if getAccount(request).getPendingResearchesCount() > mum.owner.technology.o_12:
            return HttpResponse('QUEUE')
        

    if not getRequirements(mum.owner.technology, getRace(request), int(request.GET['what'])).validate(mum):
        return HttpResponse('REQUIREMENTS')

    if not canAdvance(mum.owner.technology, getRace(request), int(request.GET['what'])):
        return HttpResponse('ADVANCE')

    note(request, LM_RESEARCH_ORDERED, mid=mum.id,
                                       what=int(request.GET['what']),
                                       levelfrom=mum.owner.technology.__dict__['o_'+request.GET['what']])
    
    orderResearch(mum, int(request.GET['what']), costs)
    return HttpResponse('OK')
    
