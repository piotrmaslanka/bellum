# coding=UTF-8
from djangomako.shortcuts import render_to_response
from bellum.common.session.login import must_be_logged
from bellum.alliance.models import AllianceMembership
from bellum.alliance import mine_alliance
from bellum.common.gui import PrimaryGUIObject

@must_be_logged
@mine_alliance
def process(request, membership):
    return render_to_response('alliance/members/list.html',
                             {'pgo':PrimaryGUIObject(request),
                              'entries':AllianceMembership.objects.filter(alliance=membership.alliance),
                              'membership':membership})