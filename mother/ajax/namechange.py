# coding=UTF-8
from django.http import HttpResponse
from bellum.common.session.login import must_be_logged_ajax
from bellum.common.session.mother import getCurrentMother
from bellum.stats.larf import note
from bellum.stats.larf.const import LM_NAMECHANGE

@must_be_logged_ajax
def process(request):
    '''Checks whether the name is valid, and if possible, changes it'''
    mum = getCurrentMother(request)

    if request.GET['name'].strip() in ('', u''):
        return HttpResponse('')

    note(request, LM_NAMECHANGE, mid=mum.id,
                                 old=mum.name,
                                 new=request.GET['name'])

    mum.name = request.GET['name']
    mum.save()
    
    return HttpResponse(mum.name)
    
