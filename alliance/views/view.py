# coding=UTF-8
from django.shortcuts import redirect
from djangomako.shortcuts import render_to_response
from bellum.register.models import Account
from bellum.common.session.login import must_be_logged
from bellum.common.session import getAccountId, getAccount
from bellum.alliance.models import Alliance, AllianceMembership
from bellum.alliance.models import AM_TEAMSITE, AM_PRIVILEGE, AM_KICK, AM_ACCEPT
from bellum.alliance import mine_alliance
from bellum.common.gui import PrimaryGUIObject
from django import forms

@must_be_logged
def other(request, alliance_id):
    try:
        all = Alliance.objects.get(id=int(alliance_id))
    except:
        return redirect('/register/login/')
    return render_to_response('alliance/view/other.html',
                             {'alliance':all,
                             'pgo':PrimaryGUIObject(request)})

@must_be_logged
@mine_alliance
def own(request, membership):
    return render_to_response('alliance/view/own.html',
                             {'alliance':membership.alliance,
                             'membership':membership,
                             'pgo':PrimaryGUIObject(request)})