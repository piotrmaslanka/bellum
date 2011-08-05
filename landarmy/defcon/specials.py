class SpecialRule(object): pass
class ParametricSpecialRule(SpecialRule):
    def __init__(self, x): self.x = x

class DefensiveDrones(SpecialRule):            # fixed to unit
    '''Each turn, adds 1 defensive drone to my army'''
class DebrisMaker(ParametricSpecialRule):                     # fixed to unit
    '''When the unit dies, substract x max debris from me'''
class WhatAMess(ParametricSpecialRule):                       # fixed to weapon
    '''When the weapon fires, add x max debris to enemy'''
class IgnoresDebris(SpecialRule):           # fixed to weapon
    '''Still substracts debris, but ignores its effects'''
class WKM(SpecialRule):                     # fixed to weapon
    '''When the weapon hits, substract one max debris point from enemy'''
class Tarpit(SpecialRule):                  # fixed to unit
    '''When unit with this rule dies, any further shots from offending weapon are mitigated in this turn(ie. AOS is forced to zero)'''
class Markerlights(ParametricSpecialRule):   # fixed to unit
    '''Adds x markerlight points to enemy army each turn'''
class OwnPace(SpecialRule):                 # fixed to unit
    '''Fires on odd turns'''
class SuicideExplosion(SpecialRule):        # fixed to weapon
    '''Fixed to unit'''
class Grenades(ParametricSpecialRule):      # fixed to weapon
    '''When hits, fires additional anti-infantry ST=1, MS=1, AOS=x shots'''
class PartyArtillery(SpecialRule):          # fixed to unit
    '''A particularly funny random behaviour'''
# special
class SkipBecauseGrenades(SpecialRule):
    '''If passed back due to received fire, cancel firing grenades due to GRENADES rule'''