from __future__ import division
from math import pow

def getRelocationTime(mother, race, planet1, planet2):
    mod = pow(0.95, mother.owner.technology.o_4)    # engineering
    mod *= pow(0.95, mother.b_0)                    # engine
    if race == 1:
        mod *= pow(0.9, mother.owner.technology.o_13)
            # racial - magnuss - SM speed

    return (planet1.distance(planet2)) * 1200 * mod

