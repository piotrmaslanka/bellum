# coding=UTF-8
from bellum.common.models import ResourceIndex, Requirement
from bellum.meta import MBI

REQUIREMENTS = (Requirement(),  # engine
                Requirement(),  # quarters
                Requirement(),  # dust collector
                Requirement(),  # armory
                Requirement(),  # lab
                Requirement(),  # hangar
                )

CONSTRUCTION_NAMES = (
    u'Silnik',
    u'Kwatery',
    u'Kolektor pyłu',
    u'Zbrojownia',
    u'Laboratorium',
    u'Hangar',
)

DESCRIPTIONS = (
    u'Zmniejsza czas relokacji HQ o 5% na poziom',
    u'Zmniejsza czas desantu/ewakuacji o 5% na poziom. Zwiększa przyrost Manpower.',
    u'Zwiększa przyrost Tytanu i Plutonu',
    u'Zmniejsza o 5% na poziom czas potrzebny na szkolenie żołnierzy',
    u'Pozwala rozwijać bardziej zaawansowane technologie',
    u'Redukuje o 10% czas zrzutu i ewakuacji',
)

_costs = {0: (ResourceIndex(titan=500, pluton=300, men=90), 600), # engine
          1: (ResourceIndex(titan=450, pluton=180, men=40), 480), # quarters
          2: (ResourceIndex(titan=300, pluton=150, men=20), 480), # dust collector
          3: (ResourceIndex(titan=800, pluton=600, men=100), 900), # armory
          4: (ResourceIndex(titan=1000, pluton=500, men=200), 1200), # lab
          5: (ResourceIndex(titan=700, pluton=500, men=20), 900), # hangar
          }

def getCosts(mother, race, what):
    from math import pow
    coef = pow(1.5, mother.__dict__['b_'+str(what)])
    tcoef = pow(0.95, mother.owner.technology.o_4)
    return (_costs[what][0]*coef, _costs[what][1]*coef*tcoef)
def getRequirements(mother, race, what):
    return REQUIREMENTS[what]
def getRequirementsArray(mother, race):
    reqs = []
    for i in xrange(0, MBI+1):
        reqs.append(getRequirements(mother, race, i))
    return reqs
def getCostsArray(mother, race):
    cost = []
    for x in xrange(0, MBI+1):
        cost.append(getCosts(mother, race, x))
    return cost