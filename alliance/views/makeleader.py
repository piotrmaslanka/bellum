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
from django.http import HttpResponse
from bellum.stats.larf import note
from bellum.stats.larf.const import LA_MADE_LEADER
from bellum.common.smf.processes import makeLeader

@must_be_logged
@mine_alliance
def process(request, membership, target_membership_id):
    try:
        tm = AllianceMembership.objects.get(id=int(target_membership_id))
    except:
        return HttpResponse('INVALIDMEMBERSHIP')
    if membership.alliance.leader.id != getAccountId(request):
        return HttpResponse('YOURENOTLEADER')
    if tm.alliance != membership.alliance:
        return HttpResponse('WRONGALLIANCE')
    if tm.account == membership.alliance.leader:
        return HttpResponse('TARGETISLEADER')

    makeLeader(membership.alliance, tm.account)

    note(request, LA_MADE_LEADER, name=membership.alliance.name,
                                  shname=membership.alliance.shname,
                                  aid=membership.alliance.id,
                                  oldleader=membership.account.id,
                                  newleader=tm.account.id)
    tm.privileges = 255
    tm.save()

    all = membership.alliance
    all.leader = tm.account
    all.save()
    return HttpResponse('OK')
