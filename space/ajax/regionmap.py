from djangomako.shortcuts import render_to_string
from bellum.common.session.login import must_be_logged
from bellum.common.session import getAccount, getRace
from bellum.province.models import Province, Reinforcement
from bellum.meta import MPBI
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from bellum.space.models import Planet

QRADIUS = 10 + 1    # 10 leftside, 10 rightside. +1 is just a modifier for the maths

def p_secm(request, x, y):
    '''Generate sector map'''
    planets = Planet.objects.filter(        # might even not exist. We don't care.
                            Q(x__gt=x-QRADIUS) & Q(x__lt=x+QRADIUS) &
                            Q(y__gt=y-QRADIUS) & Q(y__lt=y+QRADIUS)
                                 )
    return render_to_string('space/regionmap/generator/sector.html', {'x':x, 'y':y, 'planets':planets})


def p_regm(request, bx, by):
    '''Generate region map'''
    return render_to_string('space/regionmap/generator/region.html', {'bx':bx, 'by':by})

def p_galm(request):
    '''Generate galaxy map'''
    return render_to_string('space/regionmap/generator/galaxy.html', {})

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> ENTRY POINTS ( DXInterface for AJAX )

@must_be_logged
def sector_map(request):
    try:
        x = int(request.GET['x'])
        y = int(request.GET['y'])
    except:
        return HttpResponse('FAIL')
    return HttpResponse(p_secm(request, x, y).decode('utf8'))
def region_map(request):
    try:
        x = int(request.GET['x'])
        y = int(request.GET['y'])
    except:
        return HttpResponse('FAIL')
    return HttpResponse(p_regm(request, x, y).decode('utf8'))
def galaxy_map(request):
    return HttpResponse(p_galm(request).decode('utf8'))
