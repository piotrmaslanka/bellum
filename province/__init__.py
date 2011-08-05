'''This application provides only AJAX and models'''
from django.http import HttpResponse
from bellum.province.models import ProvintionalPresence, Province

def pp_available(proc):
    def pp_available_decorator(*args, **kwargs):
        try:
            pp = ProvintionalPresence.objects.get(id=int(args[0].GET['pp']))
        except:
            return HttpResponse('/')
        return proc(args[0], pp, *args[1:], **kwargs)
    return pp_available_decorator

def p_available(proc):
    def p_available_decorator(*args, **kwargs):
        try:
            pp = Province.objects.get(id=int(args[0].GET['p']))
        except:
            return HttpResponse('/')
        return proc(args[0], pp, *args[1:], **kwargs)
    return p_available_decorator
