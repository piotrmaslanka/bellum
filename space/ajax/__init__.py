from django.http import HttpResponse
from bellum.province.models import Province

def p_available(proc):
    def p_available_decorator(*args, **kwargs):
        try:
            pp = Province.objects.get(id=int(args[0].GET['p']))
        except:
            return HttpResponse('/')
        return proc(args[0], pp, *args[1:], **kwargs)
    return p_available_decorator
