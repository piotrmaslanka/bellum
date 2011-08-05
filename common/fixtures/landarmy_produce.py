from bellum.common.models import Requirement, ResourceIndex
from math import pow
from copy import copy

COSTS = \
(
    # Party
    (
        (ResourceIndex(titan=100, pluton=50, men=1), 180),
        (ResourceIndex(titan=150, pluton=50, men=3), 300),
        (ResourceIndex(titan=300, pluton=350, men=25), 300),
        (ResourceIndex(titan=400, pluton=500, men=30), 480),
        (ResourceIndex(titan=250, pluton=120, men=15), 360),
        (ResourceIndex(titan=800, pluton=400, men=120), 420),
        (ResourceIndex(titan=120, pluton=650, men=220), 600),
        (ResourceIndex(titan=600, pluton=330, men=20), 360),
        (ResourceIndex(titan=750, pluton=330, men=45), 420),
        (ResourceIndex(titan=1500, pluton=1000, men=350), 900),
    ),
    # Magnuss
    (
        (ResourceIndex(titan=150, pluton=80, men=1), 240),
        (ResourceIndex(titan=300, pluton=150, men=5), 300),
        (ResourceIndex(titan=445, pluton=300, men=15), 420),
        (ResourceIndex(titan=375, pluton=255, men=15), 480),
        (ResourceIndex(titan=520, pluton=480, men=35), 600),
        (ResourceIndex(titan=600, pluton=300, men=20), 420),
        (ResourceIndex(titan=1500, pluton=650, men=210), 600),
        (ResourceIndex(titan=800, pluton=400, men=55), 660),
        (ResourceIndex(titan=300, pluton=120, men=10), 180),
        (ResourceIndex(titan=2500, pluton=880, men=420), 1200),
    ),
    # Teknishon
    (
        (ResourceIndex(titan=150, pluton=200, men=5), 240),
        (ResourceIndex(titan=150, pluton=100, men=2), 300),
        (ResourceIndex(titan=300, pluton=300, men=5), 300),
        (ResourceIndex(titan=575, pluton=350, men=25), 420),
        (ResourceIndex(titan=1200, pluton=600, men=120), 600),
        (ResourceIndex(titan=1500, pluton=800, men=420), 1200),
        (ResourceIndex(titan=600, pluton=450, men=15), 180),
        (ResourceIndex(titan=600, pluton=350, men=30), 420),
        (ResourceIndex(titan=2000, pluton=1300, men=620), 1500),
        (ResourceIndex(titan=900, pluton=1100, men=450), 900),
    ),
)

def getCosts(mother, race, id):
    mc = COSTS[race][id]
    mc = list(mc)
    mc[0] = copy(mc[0])
    mc[1] *= pow(0.95, mother.b_3)                      # armory
    mc[1] *= pow(0.95, mother.owner.technology.o_10)    # logistics
    if race == 0:
        mc[0] *= pow(0.98, mother.owner.technology.o_13)
            # racial - party - cost reduction
    return mc

REQS = \
(
    # Party
    (
        Requirement(),
        Requirement(t_0=1, t_7=2),
        Requirement(t_7=3),
        Requirement(t_7=2, t_9=1),
        Requirement(t_9=1, t_0=2),
        Requirement(t_8=2),
        Requirement(t_9=2, t_7=3),
        Requirement(t_0=2),
        Requirement(t_8=3),
        Requirement(t_8=5, t_7=5)
    ),
    # Magnuss
    (
        Requirement(),
        Requirement(t_7=2),
        Requirement(t_7=4, t_0=2),
        Requirement(t_7=3, t_9=2),
        Requirement(t_7=2, t_9=1),
        Requirement(t_0=2, t_9=3),
        Requirement(t_7=5, t_8=1),
        Requirement(t_7=4, t_0=3, t_9=3),
        Requirement(t_9=5, t_10=5, t_4=5),
        Requirement(t_7=5, t_8=3, t_9=3),
    ),
    # Teknishon
    (
        Requirement(t_0=2),
        Requirement(),
        Requirement(t_0=3),
        Requirement(t_7=3, t_0=4),
        Requirement(t_7=5, t_9=2),
        Requirement(t_8=2, t_9=4),
        Requirement(t_8=3, t_7=3, t_9=2),
        Requirement(t_9=6),
        Requirement(t_7=5, t_8=7, t_9=3),
        Requirement(t_7=4, t_4=5),
    ),
)

def getRequirements(mother, race, id):
    return REQS[race][id]
    
