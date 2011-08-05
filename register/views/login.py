# coding=UTF-8
from django.http import HttpResponse
from django.shortcuts import redirect
from djangomako.shortcuts import render_to_response
from django import forms
from bellum.register.models import Account
from datetime import datetime
from bellum.common.session.login import sessLogin, isLogged
from hashlib import sha1

class LoginForm(forms.Form):
    '''Form used in logon script'''
    login = forms.CharField(label='Login', max_length=20, required=False)
    password = forms.CharField(label='Hasło', max_length=40, widget=forms.PasswordInput, required=False)
    
    def clean(self):
        '''Checks whether the login and password are valid'''
        
        try:
            acc, = Account.objects.filter(login=self.cleaned_data['login']).filter(password=sha1(self.cleaned_data['login'].encode('utf8').lower()+self.cleaned_data['password'].encode('utf8')).hexdigest())
        except ValueError:
            raise forms.ValidationError('INVALID_DATA')
        except KeyError:
            return self.cleaned_data
        
        try:
            acc.registerconfirmation_set.all()[0]
        except:
            return self.cleaned_data
        else:
            raise forms.ValidationError('INACTIVE')
        
        return self.cleaned_data     

def process(request):

    if isLogged(request):
        return redirect('/stats/empire')

    if request.method == 'POST':
        lf = LoginForm(request.POST)
        if lf.is_valid():
            acc = Account.objects.get(login=lf.cleaned_data['login'])
            if acc.banexpire != None:
                if acc.banexpire < datetime.now():
                    acc.banexpire = None
                    acc.save()
                else:
                    return render_to_response('register/login/login.html', {'form':lf,
                                                                            'banned':True,
                                                                            'bannedto':acc.banexpire,
                                                                            'banreason':acc.banreason})
            sessLogin(acc, request)
            return redirect('/stats/empire/')
    try:
        lf
    except:
        lf = LoginForm()        
    
    return render_to_response('register/login/login.html', {'form':lf, 'banned':False})
    
