# coding=UTF-8
from django.shortcuts import redirect
from djangomako.shortcuts import render_to_response
from bellum.register.models import Account
from bellum.common.session.login import must_be_logged
from bellum.common.session import getAccountId, getAccount
from bellum.alliance.models import Alliance, AllianceApplication
from bellum.alliance import has_not_alliance
from bellum.common.gui import PrimaryGUIObject
from django import forms
from bellum.stats.larf.const import LA_APPLIED_TO_ALLIANCE
from django.http import HttpResponse
from bellum.stats.larf import note
from django.core.exceptions import ObjectDoesNotExist

@must_be_logged
def cancel(request):
    try:
        aap = AllianceApplication.objects.get(applicant=getAccount(request))
    except ObjectDoesNotExist:
        return HttpResponse('FAIL')
    else:
        aap.delete()
        return HttpResponse('OK')
    

@must_be_logged
@has_not_alliance
def process(request, alliance_id):
    try:
        alliance = Alliance.objects.get(id=int(alliance_id))
    except ObjectDoesNotExist:
        return redirect('/register/login/')
    try:
        aap = AllianceApplication.objects.get(applicant=getAccount(request))
    except ObjectDoesNotExist:
        pass
    else:
        return render_to_response('alliance/apply/applying.html',
                             {'pgo':PrimaryGUIObject(request),
                              'alliance':alliance})


    if request.method == 'POST':
        if len(request.POST['text']) > 128000: request.POST['text'] = request.POST['text'][:128000]
        aa = AllianceApplication(None,
                                 getAccountId(request),
                                 alliance_id,
                                 request.POST['text'])
        aa.save()
        note(request, LA_APPLIED_TO_ALLIANCE, name=alliance.name,
                                              shname=alliance.shname,
                                              aid=alliance.id,
                                              accid=getAccountId(request),
                                              message=request.POST['text'])
        return redirect('/alliance/view/'+str(alliance.id)+'/')

    return render_to_response('alliance/apply/form.html',
                             {'pgo':PrimaryGUIObject(request),
                              'alliance':alliance})