# coding=UTF-8
from django.shortcuts import redirect
from djangomako.shortcuts import render_to_response
from bellum.register.models import Account
from bellum.common.session.login import must_be_logged
from bellum.common.session import getAccountId, getAccount
from bellum.alliance.models import Alliance, AllianceMembership, LAM_CHOICES, AM_PRIVILEGE, AM_TEAMSITE, AM_ACCEPT, AM_KICK, AM_MODERATE
from bellum.alliance import mine_alliance
from bellum.common.gui import PrimaryGUIObject
from django import forms
from django.http import HttpResponse
from bellum.stats.larf.const import LA_APPLIED_TO_ALLIANCE
from bellum.stats.larf import note
from django.core.exceptions import ObjectDoesNotExist
from django.utils.html import escape
from bellum.common.smf.processes import makeModerator, removeModerator

@must_be_logged
@mine_alliance
def rank(request, membership, target_membership_id):        # supply new rank via GET:rank
    target_membership_id = int(target_membership_id)
    try:
        tm = AllianceMembership.objects.get(id=target_membership_id)
    except ObjectDoesNotExist:
        return HttpResponse('INVALID MEMBERSHIP')

    if tm.alliance != membership.alliance:
        return HttpResponse(escape(tm.rank))

    if (tm.account == membership.alliance.leader):          # if you change leader rank
        if not (getAccount(request) == membership.alliance.leader):    # you must be the leader
            return HttpResponse(escape(tm.rank))

    if not membership.hasPrivilege(AM_PRIVILEGE):
        return HttpResponse(escape(tm.rank))

    tm.rank = request.GET['rank']

    try:
        tm.save()
    except:
        pass

    return HttpResponse(escape(tm.rank))

@must_be_logged
@mine_alliance
def toggle(request, membership, target_membership_id, priv_id):
    target_membership_id = int(target_membership_id)
    priv_id = int(priv_id)
    try:
        tm = AllianceMembership.objects.get(id=target_membership_id)
    except ObjectDoesNotExist:
        return HttpResponse('INVALID MEMBERSHIP')

    if tm.alliance != membership.alliance:
        return HttpResponse('INVALID ALLIANCE')

    if tm.account == membership.alliance.leader:
        return HttpResponse('IS A LEADER')

    if not (priv_id in (AM_KICK, AM_ACCEPT, AM_PRIVILEGE, AM_TEAMSITE, AM_MODERATE)):
        raise Exception
        return HttpResponse('INVALID PRIVILEGE ID')

    if not membership.hasPrivilege(AM_PRIVILEGE):
        return HttpResponse('NOT PRIVILEGED')

    if tm.hasPrivilege(AM_MODERATE):
        removeModerator(tm.alliance, tm.account)

    if tm.hasPrivilege(priv_id):        # taking away
        if priv_id == AM_MODERATE: removeModerator(tm.alliance, tm.account)
        added = 0
        tm.privileges -= priv_id
    else:                               # giving
        if priv_id == AM_MODERATE: makeModerator(tm.alliance, tm.account)
        added = 1
        tm.privileges += priv_id
    tm.save()
    return HttpResponse(added)