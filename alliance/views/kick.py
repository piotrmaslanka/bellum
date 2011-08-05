# coding=UTF-8
from django.shortcuts import redirect
from djangomako.shortcuts import render_to_response
from bellum.register.models import Account
from bellum.common.session.login import must_be_logged
from bellum.common.session import getAccountId, getAccount
from bellum.alliance.models import Alliance, AllianceMembership, AllianceApplication
from bellum.alliance.models import AM_KICK
from bellum.alliance import mine_alliance
from bellum.common.gui import PrimaryGUIObject
from django import forms
from bellum.stats.larf import note
from bellum.stats.larf.const import LA_KICKED_FROM_ALLIANCE
from django.http import HttpResponse
from bellum.common.smf.processes import bootFromAlliance

@must_be_logged
@mine_alliance
def process(request, membership, target_membership_id):
    if not membership.hasPrivilege(AM_KICK):
        return HttpResponse('YOU CANT KICK')

    try:
        tm = AllianceMembership.objects.get(id=int(target_membership_id))
    except ObjectDoesNotExist:
        return HttpResponse('INVALID PLAYER')

    if tm.alliance != membership.alliance:
        return HttpResponse('CANT KICK FROM OTHER ALLIANCE')

    if tm.account == membership.alliance.leader:
        return HttpResponse('CANT KICK LEADER')
    
    note(request, LA_KICKED_FROM_ALLIANCE, name=membership.alliance.name,
                                           shname=membership.alliance.shname,
                                           aid=membership.alliance.id,
                                           kicker=membership.account.id,
                                           kickee=tm.account.id)

    bootFromAlliance(tm.alliance, tm.account)

    tm.delete()
    all = membership.alliance
    all.members -= 1
    all.save()
    return HttpResponse('OK')