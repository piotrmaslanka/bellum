# coding=UTF-8
from django.http import HttpResponse
from django.shortcuts import redirect
from djangomako.shortcuts import render_to_response, render_to_string
from django import forms
from django.db import IntegrityError
from bellum.register.models import Account, PasswordRemindToken
from hashlib import sha1
from datetime import datetime, timedelta
from django.core.exceptions import ObjectDoesNotExist
from bellum.common.utils.mail import send
from bellum.common.smf import changepassword

class RemindForm(forms.Form):
    '''Form used to get e-mail for remindering'''
    email = forms.EmailField(label=u'Email', error_messages={'required':u'To pole jest wymagane','invalid':u'Niepoprawny e-mail!'})

    def clean(self):
        cleaned_data = super(RemindForm, self).clean()

        try:
            acce = Account.objects.get(email=cleaned_data['email'])
        except ObjectDoesNotExist:
            raise forms.ValidationError, u'Ten adres e-mail nie istnieje w naszej bazie'
        except:
            raise forms.ValidationError, u'Niepoprawny e-mail!'
        if None == acce.resources:
            raise forms.ValidationError, u'Konto nie jest aktywne!'

        return cleaned_data

def sup(x):
    try:
        return x.errors[0]
    except:
        return ''


def process(request):
    if request.method == 'POST':
        rf = RemindForm(request.POST)
        if rf.is_valid():
            acc = Account.objects.get(email=rf.cleaned_data['email'])
            if acc.passwordremindtoken_set.count() > 0:
                acc.passwordremindtoken_set.all().delete()
                didRemovePrevious = True
            else:
                didRemovePrevious = False
            prt = PasswordRemindToken(account=acc)

            prt.key = sha1(str(datetime.now()) + 'thelightwasbrighter').hexdigest()
            while True:     # Make it so key is truly unique
                try:
                    prt.save()      # chance is 1:2^160 that key repeats, but the chance is
                except IntegrityError:
                    prt.key = sha1(prt.key + 'hellocharlie' + str(datetime.now())).hexdigest()
                else:
                    break
            try:
                resp = render_to_string('register/passremind/mail.txt', {'key':prt.key,
                                                                         'login':acc.login,
                                                                         'accname':acc.empire,
                                                                         'newpass':prt.newpassword})
                send(acc.email, u'Bellum - przypomnienie hasła', unicode(resp, 'UTF-8'))
            except Exception, e:
                # something has FEHLED
                prt.delete()
                raise e
            return render_to_response('register/passremind/success.html', {'key':prt.key,
                                                            'newpassword':prt.newpassword,
                                                            'didRemovePrevious':didRemovePrevious})
    try:
        rf
    except:
        rf = RemindForm()

    return render_to_response('register/passremind/form.html', {'form':rf, 'sup':sup})

def activate(request):
    try:
        prt = PasswordRemindToken.objects.get(key=request.GET['key'])
    except:
        return render_to_response('register/passremind/activate.html', {'success':False,
                                                                        'error':'notfound'})

    if (datetime.now() - prt.generated_on) > timedelta(7):          # older than 7 days?
        prt.delete()
        return render_to_response('register/passremind/activate.html', {'success':False,
                                                                        'error':'old'})

    newpass = prt.newpassword       # newpass is ASCII-safe but needs encode for everything to be ASCII
    prt.account.password = sha1(prt.account.login.lower().encode('utf8')+newpass.encode('utf8')).hexdigest()
    prt.account.save()
    prt.delete()
    changepassword(prt.account.login, prt.account.password)

    return render_to_response('register/passremind/activate.html', {'success':True,
                                                                    'newpassword':newpass})

