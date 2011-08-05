# coding=UTF-8
from django.http import HttpResponse
from django.shortcuts import redirect
from djangomako.shortcuts import render_to_response, render_to_string
from django import forms
from bellum.register.models import Account, RegisterConfirmation
from django.db import IntegrityError
from hashlib import sha1
from datetime import datetime
from bellum.common.utils.mail import send
from bellum.common.smf import username_taken, empire_taken
from django.utils.html import strip_tags

class RegisterForm(forms.ModelForm):
    '''Form used to register new users'''
    password = forms.CharField(label='Hasło', max_length=40, error_messages={'required':"To pole jest wymagane"}, widget=forms.PasswordInput)
    password2 = forms.CharField(label='Powtórz hasło', max_length=40, error_messages={'required':'To pole jest wymagane'}, widget=forms.PasswordInput)

    class Meta:
        model = Account
        exclude = ('points', 'signature', 'sex', 'birthdate', 'banreason', 'banexpire', 'priv', 'registered_on', 'is_avatar')
        fields = ('login', 'password', 'password2', 'race', 'email', 'empire')
        
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['login'].error_messages = {'required': u"To pole jest wymagane",
                                               'unique': u"Login już używany"}
        self.fields['email'].error_messages = {'required':u"To pole jest wymagane",
                                               'invalid':u"Niepoprawny e-mail"}
        self.fields['password'].error_messages = {'required': u"Pole wymagane", }
        self.fields['empire'].error_messages = {'required': u"To pole jest wymagane",
                                               'unique':u"Nazwa imperium zajęta", }
    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()

        try:
            if strip_tags(cleaned_data['login']) != cleaned_data['login']:
                self._errors['login'] = forms.util.ErrorList([u'Tylko bez sztuczek, OK?'])
        except:
            pass

        try:
            if strip_tags(cleaned_data['empire']) != cleaned_data['empire']:
                self._errors['empire'] = forms.util.ErrorList([u'Tylko bez sztuczek, OK?'])
        except:
            pass

        try:
            if cleaned_data['password'] != cleaned_data['password2']:
                self._errors['password'] = forms.util.ErrorList([u'Hasła nie zgadzają się'])
        except KeyError:
            pass

        try:
            if username_taken(cleaned_data['login']):   # check linked forum
                self._errors['login'] = forms.util.ErrorList([u'Login już używany'])
        except:
            pass

        try:
            if empire_taken(cleaned_data['empire']):    # check linked forum
                self._errors['empire'] = forms.util.ErrorList([u'Nazwa już używana'])
        except:
            pass
        
            # Quick hack. Django doesn't seem to solve the unique naming stuff
        for k, v in self._errors.iteritems():
            if v[0][0:19] == 'Account with this L':
                self._errors[k] = forms.util.ErrorList([u'Login jest już uzywany'])
            if v[0][0:21] == 'Account with this Emp':
                self._errors[k] = forms.util.ErrorList([u'Nazwa imperium zajęta'])
            if v[0][0:21] == 'Account with this Ema':
                self._errors[k] = forms.util.ErrorList([u'Ten email jest już w bazie!'])
        
        return cleaned_data

def sup(x):
    try:
        return x.errors[0]
    except:
        return ''

def process(request):
    if request.method == 'POST':
        rf = RegisterForm(request.POST)
        if rf.is_valid():
            account = rf.save(commit=False)
            account.password = sha1(rf.cleaned_data['login'].encode('utf-8').lower()+rf.cleaned_data['password'].encode('utf-8')).hexdigest()

            account.id = None
            account.save()
           
            rc = RegisterConfirmation()
            rc.account = account
            rc.key = sha1(str(datetime.now()) + 'ourwearyeyesstillstraytothehorizon').hexdigest()
            while True:     # Make it so key is truly unique
                try:
                    rc.save()
                except IntegrityError:
                    rc.key = sha1(rc.key + 'theteaset' + str(datetime.now())).hexdigest()
                else:
                    break

            resp = render_to_string('register/register/mail.txt', {'key':rc.key,
                                                                   'password':rf.cleaned_data['password'],
                                                                   'login':account.login,
                                                                   'empire':account.empire})
            send(account.email, u'Bellum - aktywacja konta', unicode(resp, 'UTF-8'))

            return render_to_response('register/register/success.html', {})
       
    try:
        rf
    except:
        rf = RegisterForm()
   
    return render_to_response('register/register/register.html', {'form':rf, 'sup':sup})
