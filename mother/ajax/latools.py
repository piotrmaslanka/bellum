# coding=UTF-8
'''Suite of AJAX tools to do with Research'''
from django.http import HttpResponse
from bellum.common.session.login import must_be_logged_ajax 
from bellum.common.session import getAccount, getResourceIndex, getRace
from bellum.common.session.mother import getCurrentMother
from bellum.common.fixtures.landarmy_produce import getRequirements, getCosts
from datetime import datetime
from bellum.orders.mother.landarmy_build import orderProduce
from bellum.stats.larf import note
from bellum.meta import MGID
from bellum.stats.larf.const import LM_LANDARMY_TRAINING

@must_be_logged_ajax
def order(request):
    '''Starts building land army units
            When:
                    Resources met
                    Requirements met'''
                    
    mum = getCurrentMother(request)
        # Python will HTTP 500 on invalid GET data
    costs = getCosts(mum, getRace(request), int(request.GET['what'])) 
    
    if not (int(request.GET['what']) in range(0,MGID+1)): return HttpResponse('WHATINVALID')

    if int(request.GET['amount']) < 1: return HttpResponse('INVALIDAMOUNT')

    if costs[0]*int(request.GET['amount']) > getResourceIndex(request).stateUpdate():
        return HttpResponse('COSTS')
    if not getRequirements(mum, getRace(request), int(request.GET['what'])):
        return HttpResponse('REQUIREMENTS')
    
    note(request, LM_LANDARMY_TRAINING, mid=mum.id,
                                        what=int(request.GET['what']),
                                        amount=int(request.GET['amount']))
    
    orderProduce(mum, getRace(request), int(request.GET['what']), int(request.GET['amount']))
    return HttpResponse('OK')