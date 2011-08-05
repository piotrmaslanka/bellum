# coding=UTF-8
from django.shortcuts import redirect
from djangomako.shortcuts import render_to_response
from bellum.register.models import Account
from bellum.mother.models import Mother
from bellum.common.session.mother import getCurrentMother
from bellum.common.session.login import must_be_logged_ajax
from bellum.common.session import getAccount,  getResourceIndex
from bellum.common.gui import PrimaryGUIObject
from bellum.common.models import ResourceIndex
from bellum.orders.mother.resources import orderResourceSend
from django import forms
from bellum.stats.larf import note
from bellum.stats.larf.const import LM_SENT_RESOURCE
from django.http import HttpResponse

@must_be_logged_ajax
def process(request):
    try:
        titan = int(request.GET['titan'])
    except:
        titan = 0

    try:
        pluton = int(request.GET['pluton'])
    except:
        pluton = 0

    try:
        manpower = int(request.GET['men'])
    except:
        manpower = 0

    try:
        target = Account.objects.get(id=int(request.GET['target']))
    except:
        return HttpResponse('FAIL')

    my_mum = getCurrentMother(request)

    acc = getAccount(request)
    if acc == target: return HttpResponse('SELF')

    rindex = getResourceIndex(request)
    rindex.stateUpdate()

    sending_res = ResourceIndex(titan=titan, pluton=pluton, men=manpower)
    if (sending_res == 0): return HttpResponse('NULL')
    if (sending_res > rindex): return HttpResponse('TOOMUCH')

    tg_mother = Mother.objects.get(owner=target)
    note(request, LM_SENT_RESOURCE, mid=my_mum.id,
                                    target=tg_mother.id,
                                    resources=sending_res)

    orderResourceSend(my_mum, tg_mother, sending_res.titan, sending_res.pluton, sending_res.men)

    return HttpResponse('OK')
