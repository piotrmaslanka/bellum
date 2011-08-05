# coding=UTF-8
from django.shortcuts import redirect
from djangomako.shortcuts import render_to_response
from bellum.register.models import Account
from bellum.common.session.login import must_be_logged
from bellum.common.session import getAccountId, getAccount
from bellum.alliance.models import Alliance, AllianceMembership, AllianceApplication
from bellum.alliance.models import AM_TEAMSITE, AM_PRIVILEGE, AM_KICK, AM_ACCEPT
from bellum.alliance import has_not_alliance
from bellum.common.gui import PrimaryGUIObject
from django import forms
from bellum.stats.larf.const import LA_CREATE_ALLIANCE
from bellum.stats.larf import note
from django.core.exceptions import ObjectDoesNotExist
from bellum.common.smf.processes import createAlliance

class NewAllianceForm(forms.ModelForm):
    class Meta:
        model = Alliance
        exclude = ('mainpage', 'points', 'leader', 'members', 'is_avatar', 'smf_board_id', 'smf_group_id')
        
    def __init__(self, *args, **kwargs):
        super(NewAllianceForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = u'Nazwa'
        self.fields['shname'].label = u'Skrót 5 liter'

@must_be_logged
@has_not_alliance
def process(request):
    try:
        aap = AllianceApplication.objects.get(applicant=getAccount(request))
    except ObjectDoesNotExist:
        pass
    else:
        return render_to_response('alliance/apply/applying.html',
                                 {'pgo':PrimaryGUIObject(request),
                                  'application':aap,
                                  'alliance':aap.alliance})

    if request.method == 'POST':
        af = NewAllianceForm(request.POST)
        if af.is_valid():
            group_id, board_id = createAlliance(af.cleaned_data['name'], getAccount(request))

            af.instance.name = af.cleaned_data['name']
            af.instance.shname = af.cleaned_data['shname']
            af.instance.leader = getAccount(request)
            af.instance.mainpage = u'Do ustawienia'
            af.instance.members = 1
            af.instance.smf_board_id = board_id
            af.instance.smf_group_id = group_id
            af.instance.save()
            amb = AllianceMembership(None, af.instance.leader.id, af.instance.id,
                    255,
                    u'Szef')
            amb.save()
            note(request, LA_CREATE_ALLIANCE, name=af.instance.name,
                                              shname=af.instance.shname,
                                              aid=af.instance.id)
            return redirect('/alliance/view/own/')
    try:
        af
    except:
        af = NewAllianceForm()
    return render_to_response('alliance/new/newform.html',
                             {'form':af, 'pgo':PrimaryGUIObject(request)})