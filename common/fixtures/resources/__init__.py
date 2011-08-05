from __future__ import division
from bellum.common.fixtures.resources.recalculate import recalc as _recalc
from math import pow


def recalc(*args, **kwargs):
    '''Used to retain interface compatiblity'''
    return _recalc(*args, **kwargs)

def getResourceTravelTime(mother_from, mother_to):
    '''Returns travel time in seconds, as far as normal resource transfer is considered'''

    rct = mother_from.duePosition().distance(mother_to.duePosition()) / 200

    rct = rct * pow(0.95, mother_from.b_0)       # engine

    if mother_from.owner.race == 1:
        rct = rct * pow(0.90, mother_from.owner.technology.o_15)
            # racial - magnuss - merchant ship travel time
            
    return 120 * rct