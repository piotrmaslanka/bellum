# coding=UTF-8
from django.shortcuts import redirect
from djangomako.shortcuts import render_to_response
from bellum.register.models import Account
from bellum.common.session.login import must_be_logged
from bellum.common.session import getAccountId, getAccount
from bellum.alliance.models import Alliance, AllianceMembership, AllianceApplication
from bellum.alliance.models import AM_TEAMSITE, AM_PRIVILEGE, AM_KICK, AM_ACCEPT
from bellum.alliance import mine_alliance
from bellum.common.gui import PrimaryGUIObject
from django import forms
from bellum.stats.larf import note
from bellum.stats.larf.const import LA_LEAVE_ALLIANCE
from bellum.common.smf.processes import bootFromAlliance

@must_be_logged
@mine_alliance
def process(request, membership):
    if (getAccount(request) == membership.alliance.leader):
        return HttpResponse('LEADERCANTLEAVE')
    else:
        note(request, LA_LEAVE_ALLIANCE, name=membership.alliance.name,
                                         shname=membership.alliance.shname,
                                         aid=membership.alliance.id,
                                         accid=getAccountId(request))
        membership.alliance.members -= 1
        membership.alliance.save()
        bootFromAlliance(membership.alliance, getAccount(request))
        membership.delete()
        return HttpResponse('OK')
