# coding=UTF-8
from bellum.common.models import ResourceIndex, Requirement
from bellum.meta import MTI

_costs = {0:(ResourceIndex(titan=900, pluton=900, men=100), 1500),  # infantry armor
1:(ResourceIndex(titan=60000, pluton=80000, men=20000), 36000),    # nanobot armor
2:(ResourceIndex(titan=500, pluton=400, men=100), 1200),   # excavation
3:(ResourceIndex(titan=100000, pluton=100000, men=80000), 86400),   # diamond drills
4:(ResourceIndex(titan=200, pluton=300, men=200), 1200),  # engineering
5:(ResourceIndex(titan=1800, pluton=3000, men=1400), 12000), # counterespionage
6:(ResourceIndex(titan=500, pluton=3500, men=2000), 7200), # optotechnics
7:(ResourceIndex(titan=200, pluton=1000, men=300), 1800),  # off systems
8:(ResourceIndex(titan=1000, pluton=2000, men=100), 4800),  # tank armor
9:(ResourceIndex(titan=200, pluton=1000, men=400), 7200), # support systems
10:(ResourceIndex(titan=100, pluton=200, men=400), 1800), # logistics
11:(ResourceIndex(titan=20, pluton=40, men=800), 7200), # nauka
12:(ResourceIndex(titan=100000, pluton=120000, men=250000), 129600), # supercomputer
13:None, # racial
}

TECHNOLOGY_NAMES = (
    u'Zbroja piechoty',
    u'Pancerz z nanobotów',
    u'Wydobycie',
    u'Wiertła diamentowe',
    u'Inżynieria',
    u'Kontrwywiad',
    u'Optotechnika',
    u'Systemy ofensywne',
    u'Pancerz czołgów',
    u'Wsparcie',
    u'Logistyka',
    u'Nauka',
    u'Superkomputer',
    u'Technologia rasowa',
)

GENERIC_DESCRIPTIONS = (
    u'Zwiększa wytrzymałość piechoty',
    u'Znacznie zwiększa wytrzymałość piechoty',
    u'Zwiększa o 5% na poziom wydobycie Tytanu i Plutonu',
    u'Zwiększa o 20% wydobycie Tytanu i Plutonu',
    u'Zmniejsza o 5% na poziom czas budowy na HQ. Zmniejsza o 5% czas relokacji HQ. Zmniejsza o 5% na poziom czasu budowy na prowincji.',
    u'Pozwala chronić się przed skanerami Magnuss',
    u'Zwiększa celność żołnierzy',
    u'Zwiększa atak żołnierzy i czołgów',
    u'Zwiększa wytrzymałość czołgów',
    u'Ulepsza jednostki Wsparcia',
    u'Zmniejsza o 5% na poziom czas relokacji wojsk. Zmniejsza o 5% na poziom czas szkolenia żołnierzy.',
    u'Zmniejsza o 5% cenę badań naukowych',
    u'Pozwala rozwijać więcej technologii równocześnie.',
    u'RESERVED',
)

def getTechnologyDescription(id, race):
    '''Id as in technology ID'''
    if id == 13:
        if race == 0:       # Party
            return u'Redukuje o 2% na poziom koszt szkolenia wojska. Zwiększa o 10% na poziom ataku żołnierzy.'
        if race == 1:       # Magnuss
            return u'Zmniejsza o 10% na poziom czas relokacji matki. Zmniejsza o 5% na poziom czas budowy na prowincji.'
        if race == 2:       # Teknishon
            return u'Zwiększa celność wojsk w obronie. Zwiększa osłonę podczas walki obronnej.'
    else:
        return GENERIC_DESCRIPTIONS[id]
    

def canAdvance(technology, race, what):
    if what in (1, 3):
        if technology.__dict__['o_'+str(what)] > 0:
            return False
        else:
            return True
    if what == 12:
        if technology.o_12 > 1:
            return False
        else:
            return True
    return True

def getCosts(technology, race, id):
    from math import pow
    if id == 13:
        if race == 0:   # party
            cost = (ResourceIndex(titan=3000, pluton=2000, men=1000), 14400)
        elif race == 1: # magnuss
            cost = (ResourceIndex(titan=2000, pluton=3500, men=1200), 10800)
        elif race == 2: # techno
            cost = (ResourceIndex(titan=1000, pluton=3000, men=800), 18000)
    else:
        cost = _costs[id]

    coef = pow(2, technology.__dict__['o_'+str(id)])
    sf = (cost[0]*coef, cost[1]*coef)

    return (sf[0] * pow(0.95, technology.o_11), sf[1] * pow(0.95, technology.o_13))

def getCostsArray(technology, race):
    costs = []
    for x in xrange(0, MTI+1):
        costs.append(getCosts(technology, race, x))
    return costs

def getRequirements(technology, race, id):
    if id == 0:         # infantry armor
        return Requirement(c_4=1, c_3=1)
    elif id == 1:       # nanobot armor
        return Requirement(c_4=7, t_0=5)
    elif id == 2:       # extraction
        return Requirement(c_4=2, c_2=2)
    elif id == 3:       # diamond drills
        return Requirement(c_4=8, t_2=8, c_2=5)
    elif id == 4:       # engineering
        return Requirement(c_4=3)
    elif id == 5:       # counterintelligence
        return Requirement(c_4=5, t_10=2)
    elif id == 6:       # optotechnics
        return Requirement(c_4=6, t_10=3, t_7=5)
    elif id == 7:       # off systems
        return Requirement(c_4=2, t_4=1, t_10=1)
    elif id == 8:       # tank armor
        return Requirement(c_4=5, t_0=2, t_10=2)
    elif id == 9:      # support
        return Requirement(c_4=5, t_7=3)
    elif id == 10:      # logistics
        return Requirement(c_4=3, t_4=2)
    elif id == 11:      # science
        return Requirement(c_4=3)
    elif id == 12:      # supercomputer
        return Requirement(c_4=8, t_11=8)
    elif id == 13:  # racial
        if race == 0:       # party
            return Requirement(c_3=4, c_4=3, t_10=5)
        elif race == 1:
            return Requirement(c_4=5, c_0=4)
        elif race == 2:
            return Requirement(c_4=6, t_11=4)

def getRequirementsArray(technology, race):
    return map(lambda x: getRequirements(technology, race, x), xrange(0,MTI+1))
