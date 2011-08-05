from django.shortcuts import redirect
from bellum.register.models import Account
from django.http import HttpResponse
from bellum.common.models import ResourceIndex
from bellum.mother.models import Mother, Technology

def sessLogin(account, request):
    request.session['Account.id'] = account.id
    request.session['ResourceIndex.id'] = account.resources.id
    request.session['Account.race'] = account.race
    request.session['Mother.id'] = Mother.objects.get(owner=account).id
    request.session['Technology.id'] = Technology.objects.get(owner=account).id
    request.session['ChatCache'] = {}       # account_id => empire
    
def sessLogout(request):
    del request.session['Account.id']
    request.session.flush()
    
def isLogged(request):
    try:
        request.session['Account.id']
    except:
        return False
    return True

def must_be_logged(process):
    def must_be_logged_decorator(*args, **kwargs):
        if not isLogged(args[0]):
            return redirect('/register/login/')
        return process(*args, **kwargs)
    return must_be_logged_decorator

def must_be_logged_ajax(process):
    def must_be_logged_decorator(*args, **kwargs):
        if not isLogged(args[0]):
            return HttpResponse('NOT_LOGGED')
        return process(*args, **kwargs)
    return must_be_logged_decorator
