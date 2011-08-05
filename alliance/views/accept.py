# coding=UTF-8
from django.shortcuts import redirect
from djangomako.shortcuts import render_to_response
from bellum.register.models import Account
from bellum.common.session.login import must_be_logged
from bellum.common.session import getAccountId, getAccount
from bellum.alliance.models import Alliance, AllianceApplication, AM_ACCEPT, AllianceMembership
from bellum.alliance import mine_alliance
from bellum.common.gui import PrimaryGUIObject
from django import forms
from bellum.stats.larf.const import LA_DECLINED_APPLICATION_TO_ALLIANCE, \
                                    LA_ACCEPTED_APPLICATION_TO_ALLIANCE
from bellum.stats.larf import note
from django.core.exceptions import ObjectDoesNotExist
from bellum.common.smf.processes import acceptAlliance

@must_be_logged
@mine_alliance
def approve(request, membership, application_id):
    if not membership.hasPrivilege(AM_ACCEPT):
        return redirect('/register/login/')
    try:
        app = AllianceApplication.objects.get(id=int(application_id))
    except ObjectDoesNotExist:
        return redirect('/register/login')

    note(request, LA_ACCEPTED_APPLICATION_TO_ALLIANCE, name=membership.alliance.name,
                                                       shname=membership.alliance.shname,
                                                       aid=membership.alliance.id,
                                                       accid=app.applicant.id,
                                                       playername=app.applicant.empire,
                                                       message=app.message)
    AllianceMembership(None,
                       app.applicant.id,
                       app.alliance.id,
                       0,
                       u'Nowy').save()
    alliance = membership.alliance
    alliance.members += 1
    alliance.save()
    acceptAlliance(alliance, app.applicant)
    app.delete()   
    
    return redirect('/alliance/accept/list/')


@must_be_logged
@mine_alliance
def decline(request, membership, application_id):
    if not membership.hasPrivilege(AM_ACCEPT):
        return redirect('/register/login/')
    try:
        app = AllianceApplication.objects.get(id=int(application_id))
    except ObjectDoesNotExist:
        return redirect('/register/login')

    note(request, LA_DECLINED_APPLICATION_TO_ALLIANCE, name=membership.alliance.name,
                                                       shname=membership.alliance.shname,
                                                       aid=membership.alliance.id,
                                                       accid=app.applicant.id,
                                                       playername=app.applicant.empire,
                                                       message=app.message)
    app.delete()
    return redirect('/alliance/accept/list/')

@must_be_logged
@mine_alliance
def list(request, membership):
    if not membership.hasPrivilege(AM_ACCEPT):
        return redirect('/register/login/')

    return render_to_response('alliance/accept/list.html',
                             {'pgo':PrimaryGUIObject(request),
                             'membership':membership,
                              'entries':AllianceApplication.objects.filter(alliance=membership.alliance)})