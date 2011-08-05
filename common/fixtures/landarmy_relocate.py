from bellum.meta import MGID
from bellum.common.fixtures.landarmy_stats import UNIT_BASECLASS
from bellum.landarmy.defcon.objects import INFANTRY, ARMOR, SUPPORT
from math import sqrt, pow

def _ptcount(army, race):
    pts = [0, 0, 0]     # INFANTRY / ARMOR / SUPPORT

    for x in xrange(0, MGID+1):
        pts[UNIT_BASECLASS[race][x]] += army[x]

    if race == 1:       # Magnuss Transporter reduction
        pts[INFANTRY] -= army[4]*15
        if pts[INFANTRY] < 0: pts[INFANTRY] = 0

    # Calculate points

    pts = pts[INFANTRY] + pts[ARMOR]*1.5 + pts[SUPPORT]

    if race == 1:   # Magnuss Kula reduction
        pts -= army[8]*20
        if pts < 0: pts = 0
        
    return pts


def ppstrikelen(src_prov, dst_prov, gar, orders, race=None):
    '''In seconds'''

    distance = sqrt(((src_prov.x - dst_prov.x) ** 2) + ((src_prov.y - dst_prov.y) ** 2))
    modifier = pow(0.9, src_prov.presence.owner.technology.o_10)    # Logistics

    return (distance * 40 + _ptcount(gar, race) * 4) * modifier


def mpstrikelen(mother, dst_prov, gar, orders, race=None):
    modifier = pow(0.9, mother.owner.technology.o_10 + mother.b_5)       # Logistics, Hangar

    return (1500 + _ptcount(gar, race) * 8) * modifier


def pmmovelen(src_prov, mother, gar, race=None):
    modifier = pow(0.9, mother.owner.technology.o_10 + mother.b_5)   # Logistics, Hangar

    return (1500 + _ptcount(gar, race) * 6) * modifier
