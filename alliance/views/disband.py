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
from bellum.stats.larf.const import LA_DISBAND_ALLIANCE
from django.http import HttpResponse
from bellum.common.smf.processes import bootFromAlliance, destroyAlliance

@must_be_logged
@mine_alliance
def process(request, membership):
    if not (getAccount(request) == membership.alliance.leader):
        return HttpResponse('NOT LEADER')

    alliance = membership.alliance
    note(request, LA_DISBAND_ALLIANCE, aid=alliance.id,
                                       name=alliance.name,
                                       shname=alliance.shname)
    AllianceApplication.objects.filter(alliance=alliance).delete()

    for ams in AllianceMembership.objects.filter(alliance=membership.alliance):
        bootFromAlliance(alliance, ams.account)
        ams.delete()
    destroyAlliance(alliance)
    membership.alliance.delete()
    return HttpResponse('OK')