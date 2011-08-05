# coding=UTF-8
'''Costs are in format tuple:(titan, pluton, men, time-seconds)'''
from bellum.common.models import ResourceIndex
from math import pow

_costs = {0: (None, None),       # nothing!
          1:  (ResourceIndex(titan=680, pluton=460, men=120), 315), # titan
          2:  (ResourceIndex(titan=600, pluton=560, men=200), 315), # pluton
          3:  (ResourceIndex(titan=900, pluton=40, men=250), 315), # town
          4:  (ResourceIndex(titan=30000, pluton=15000, men=5000), 18000), # radar
          5:  (ResourceIndex(titan=3000, pluton=100, men=500), 810), # fort
         }

BUILDING_NAMES = (
    u'BŁĄD! ZGŁOŚ ADMINISTRATOROWI!!!',
    u'Kopalnia tytanu',
    u'Kopalnia plutonu',
    u'Miasto',
    u'Radar',
    u'Fortyfikacje',
)

def getCosts(pp, race, level, what):
    coef = pow(1.5, level)

    tcoef = pow(0.95, pp.owner.technology.o_4) # engineering
    if race == 1:
        tcoef *= pow(0.95, pp.owner.technology.o_13)
                    # racial - magnuss - province build speedup

    return (_costs[what][0]*coef, _costs[what][1]*coef*tcoef)
