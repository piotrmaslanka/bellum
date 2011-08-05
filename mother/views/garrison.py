# coding=UTF-8
from django.shortcuts import redirect
from djangomako.shortcuts import render_to_response
from bellum.common.session.login import must_be_logged
from bellum.common.session import getRace
from bellum.common.session.mother import getCurrentMother
from bellum.common.gui import PrimaryGUIObject
from bellum.orders.models import LandarmyProduceOrder
from bellum.common.fixtures.landarmy_produce import getRequirements, getCosts
from bellum.meta import MGID

@must_be_logged
def land(request):
    mum = getCurrentMother(request)
    lpos = LandarmyProduceOrder.objects.filter(mother=mum.id).order_by('got__ordered_on')

    garn = {}
    for x in xrange(0, MGID+1):
        garn[x] = {}
        garn[x]['has'] = mum.garrison[x]
        garn[x]['creq'] = getRequirements(mum, getRace(request), x)
        garn[x]['req'] = garn[x]['creq'].validate(mum)
        garn[x]['cost'], garn[x]['time'] = getCosts(mum, getRace(request), x) 

    return render_to_response('mother/garrison/land.html', {'mother':mum,
                                                            'garn':garn,
                                                            'lpos':lpos,
                                                            'pgo':PrimaryGUIObject(request, mum)})
    