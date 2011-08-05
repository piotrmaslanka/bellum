# coding=UTF-8
from django.shortcuts import redirect
from djangomako.shortcuts import render_to_response
from bellum.register.models import Account
from bellum.common.session.login import must_be_logged
from bellum.common.session import getAccountId, getAccount
from bellum.alliance.models import Alliance, AM_TEAMSITE
from bellum.alliance import mine_alliance
from bellum.common.gui import PrimaryGUIObject
from bellum.stats.larf.const import LA_MODIFIED_TEAMSITE
from bellum.stats.larf import note
from django.core.exceptions import ObjectDoesNotExist
from django import forms
from bellum.common.utils.gfx import handle_img

class AvatarForm(forms.Form):
    avatar = forms.ImageField(required=False)

    def __init__(self, *args, **kwargs):
        super(AvatarForm, self).__init__(*args, **kwargs)
        self.fields['avatar'].error_messages = {'invalid':"Niepoprawny obraz", 'invalid_image':"Niepoprawny obraz"}

@must_be_logged
@mine_alliance
def process(request, alliance_membership, do_avatar=False):
    if not alliance_membership.hasPrivilege(AM_TEAMSITE):
        return redirect('/register/login/')

    avtchange_success = False
    if request.method == 'POST':
        if do_avatar:
            pa = AvatarForm(request.POST, request.FILES)
            if pa.is_valid():
                if handle_img(pa.cleaned_data['avatar'], alliance_membership.alliance.id, True) == 'GIF':
                    alliance_membership.alliance.is_avatar = 2
                else:
                    alliance_membership.alliance.is_avatar = 1
                alliance_membership.alliance.save()
                avtchange_success = True
        elif request.POST['mainpage'] != '':
            if len(request.POST['mainpage']) > 128000:  request.POST['mainpage'] = request.POST['mainpage'][:128000]
            alliance = alliance_membership.alliance
            note(request, LA_MODIFIED_TEAMSITE, name=alliance.name,
                                                shname=alliance.shname,
                                                aid=alliance.id,
                                                old=alliance.mainpage,
                                                current=request.POST['mainpage'])
            alliance.mainpage = request.POST['mainpage']
            alliance.save()
            return redirect('/alliance/view/own/')

    try:
        pa
    except:
        pa = AvatarForm()

    return render_to_response('alliance/teamsite/teamsite.html',
                             {'membership':alliance_membership,
                              'avtchange_success':avtchange_success,
                              'pa':pa,
                              'pgo':PrimaryGUIObject(request)})