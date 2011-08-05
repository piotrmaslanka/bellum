# coding=UTF-8

from django.shortcuts import redirect
from djangomako.shortcuts import render_to_response
from bellum.register.models import Account
from bellum.common.session.login import must_be_logged
from bellum.common.gui import PrimaryGUIObject
from bellum.common.utils.gfx import handle_img
from django.db import models
from django import forms
from hashlib import sha1
from bellum.common.smf import changepassword


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Account
        exclude = ('password', 'empire', 'login', 'race', 'email', 'points', 'banreason', 'banexpire', 'priv', 'resources', 'registered_on', 'is_avatar')
    
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['sex'].label = u'Płeć'
        self.fields['signature'].label = u'Opis'  
        self.fields['birthdate_year'].error_messages = {'invalid':'Wprowadź poprawną wartość'}
        self.fields['birthdate_month'].error_messages = {'invalid':'Wprowadź poprawną wartość'}
        self.fields['birthdate_day'].error_messages = {'invalid':'Wprowadź poprawną wartość'}
        self.fields['birthdate_year'].label = 'Rok urodzenia'
        self.fields['birthdate_month'].label = u'Miesiąc urodzenia'
        self.fields['birthdate_day'].label = u'Dzień urodzenia'

class PasswordForm(forms.Form):
    current_password = forms.CharField(widget=forms.PasswordInput, required=True)
    new_password1 = forms.CharField(widget=forms.PasswordInput, required=True)
    new_password2 = forms.CharField(widget=forms.PasswordInput, required=True)

    def __init__(self, *args, **kwargs):
        super(PasswordForm, self).__init__(*args, **kwargs)
        req_dict = {'required': u"To pole jest wymagane"}
        self.fields['current_password'].error_messages = req_dict
        self.fields['new_password1'].error_messages = req_dict
        self.fields['new_password2'].error_messages = req_dict

    def provide_account(self, account):
        self.account = account

    def clean_current_password(self):
        cp = self.cleaned_data['current_password']

        if ((sha1(self.account.login.encode('utf8').lower()+cp.encode('utf8'))).hexdigest() != self.account.password):
            raise forms.ValidationError(u'Niepoprawne hasło')
        return cp

    def clean(self):
        cleaned_data = self.cleaned_data
        pw1 = cleaned_data.get("new_password1")
        pw2 = cleaned_data.get("new_password2")
        if pw1 != pw2:
            self._errors['new_password1'] = forms.util.ErrorList([u'Hasła nie zgadzają się'])
        return cleaned_data

class AvatarForm(forms.Form):
    avatar = forms.ImageField(required=False)

    def __init__(self, *args, **kwargs):
        super(AvatarForm, self).__init__(*args, **kwargs)
        self.fields['avatar'].error_messages = {'invalid':"Niepoprawny obraz", 'invalid_image':"Niepoprawny obraz"}

@must_be_logged
def process(request, do_password=False, do_avatar=False):
    acc = Account.objects.get(id=request.session['Account.id'])

    pfochange_success = False
    pwdchange_success = False
    avtchange_success = False

    if request.method == 'POST':
        if do_password:
            ps = PasswordForm(request.POST)
            ps.provide_account(acc)
            if ps.is_valid():
                hash = sha1(acc.login.encode('utf8').lower()+ps.cleaned_data['new_password1'].encode('utf8')).hexdigest()
                acc.password = hash
                acc.save()
                changepassword(acc.login, hash)
                pwdchange_success = True
        elif do_avatar:
            pa = AvatarForm(request.POST, request.FILES)
            if pa.is_valid():
                if handle_img(pa.cleaned_data['avatar'], acc.id, False) == 'GIF':
                    acc.is_avatar = 2
                else:
                    acc.is_avatar = 1
                acc.save()
                avtchange_success = True
        else:
            pf = ProfileForm(request.POST, instance=acc)
            if pf.is_valid():
                pf.save()
                pfochange_success = True
    try:
        pf
    except:
        pf = ProfileForm(instance=acc)
    try:
        ps
    except:
        ps = PasswordForm()
    try:
        pa
    except:
        pa = AvatarForm()
    
    return render_to_response('uprofile/edit/form.html', {'form':pf,
                                                          'do_password':do_password,
                                                          'pwdchange_success':pwdchange_success,
                                                          'avtchange_success':avtchange_success,
                                                          'pfochange_success':pfochange_success,
                                                          'pform':ps,
                                                          'aform':pa,
                                                          'account':acc,
                                                          'pgo':PrimaryGUIObject(request)})
    
