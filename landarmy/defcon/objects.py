from __future__ import division
from random import uniform
from math import sqrt
from bellum.landarmy.defcon.dmath import throw
from bellum.landarmy.defcon.specials import IgnoresDebris, OwnPace
# unit types
SPECIAL = -1
INFANTRY = 0
ARMOR = 1
SUPPORT = 2
MULTIATTACK = 3 # infantry/armor
# outcomes
OUTCOME_ATTACKER_WON = True
OUTCOME_DEFENDER_WON = False
OUTCOME_STALEMATE = None

class Shot(object):
    def __init__(self, st, ms, utype, whoshoots, specialRules=()):
        '''specialRules is a tuple of SpecialRule'''
        self.st = st
        self.ms = ms
        self.whoshoots = whoshoots
        self.type = utype
        self.spec = specialRules

    def special(self, classType):
        '''classType is just a type'''
        for s in self.spec:
            if isinstance(s, classType): return s
        return False

    def __repr__(self):
        if self.type == INFANTRY:
            s = 'Anti-infantry '
        elif self.type == ARMOR:
            s = 'Anti-armor '
        s += 'ST='+str(self.st)+' MS='+str(self.ms)+' shot'
        return s
class Weapon(object):
    def __init__(self, st, ms, utype, poc=1, aos=1, specialRules=()):
        '''stuff is self-descriptive
           @type int 0 - anti-infantry, 1 - antiarmor
           @poc float probability of choose
           @sectype int type when a MULTIATTACK is fired'''
        self.type = utype
        self.st = st
        self.ms = ms
        self.spec = specialRules
        self.aos = aos
        self.poc = poc

    def special(self, classType):
        '''classType is just a type'''
        for s in self.spec:
            if isinstance(s, classType): return s
        return False

    def shot(self, whoshoots):
        return Shot(self.st, self.ms, self.type, whoshoots, self.spec)

class Unit(object):
    def __init__(self, cti, cta, initiative, utype, mt, weapons, specialRules=()):
        '''@cti float CT-infantry
           @cta float CT-armor
           @utype int  0 - infantry, 1 - armor
           @mt bool whether has multitracker
           @weapons tuple array of weapons
           @spec tuple list of special rules'''
        self.ct = (cti, cta)
        self.type = utype
        self.mt = mt
        self.initiative = initiative
        self.weapons = weapons
        self.spec = specialRules
        # build a cache because we will be deciding a lot on picking weapons
        self.cache = {
            ARMOR: filter(lambda x: x.type == ARMOR, self.weapons),
            INFANTRY: filter(lambda x: x.type == INFANTRY, self.weapons)}
        self.cache[MULTIATTACK] = self.cache[ARMOR] + self.cache[INFANTRY]

        aoc_infantry = 0
        aoc_army = 0
        aoc_both = 0
        for weapon in self.cache[INFANTRY]: aoc_infantry += weapon.poc
        for weapon in self.cache[ARMOR]: aoc_army += weapon.poc
        for weapon in self.cache[MULTIATTACK]: aoc_both += weapon.poc

        self.cache_aoc = {INFANTRY:aoc_infantry, ARMOR:aoc_army, MULTIATTACK:aoc_both}

    def special(self, classType):
        '''classType is just a type'''
        for s in self.spec:
            if isinstance(s, classType): return s
        return False

    def receiveFire(self, shot, army, canUseDebris=True, canUseMarkerlights=True):
        '''just return whether the unit would die'''
        if shot.type != self.type:
            raise Exception, 'I am '+str(self.type)+' - I cannot be targeted shot type '+str(shot.type)
                    # not a multiattack, get type prob
        if shot.whoshoots.type == SUPPORT:
            prob = self.ct[self.type]
        else:
            prob = self.ct[shot.whoshoots.type]

        prob = (prob+shot.ms)*shot.st

        if canUseDebris and (self.type == INFANTRY) and (army.debris > 0):   # apply debris if possible
            army.debris -= 1
            if shot.special(IgnoresDebris) == False:            # SPECIAL RULE: IGNORES DEBRIS
                prob = prob ** 2

        if canUseMarkerlights and (army.markerlights > 0) and (prob >= 0):  # apply markerlights if possible
            prob = sqrt(prob)
            army.markerlights -= 1

        return throw(prob / 2)

    def pickWeapon(self, can_target_armor, can_target_infantry, turn_no=0):

        if self.special(OwnPace) != False:                  # SPECIAL RULE: OWN PACE
            if (turn_no % 2) == 0:
                return None

        if can_target_armor and (not can_target_infantry):
            ttype = ARMOR
        elif (not can_target_armor) and can_target_infantry:
            ttype = INFANTRY
        elif can_target_armor and can_target_infantry:
            ttype = MULTIATTACK
        else:
            raise Exception, 'I cannot target anything! I should not be here...'

        chosen = uniform(0, self.cache_aoc[ttype])
        cumulative = 0
        indice = 0
        for weapon in self.cache[ttype]:
            cumulative += weapon.poc
            if cumulative > chosen:
                return weapon

        return None # has not chosed a gun!

    def bonus_im(self, bonus):
        '''substract bonus from current CT-armor'''
        self.ct = (self.ct[0] - bonus, self.ct[1])

    def bonus_ct(self, bonus):
        '''Bonus is 1-based!'''
        self.ct = (self.ct[0] * bonus, self.ct[1] * bonus)

    def bonus_st(self, bonus):
        '''Bonus is 1-based!'''
        for weapon in self.weapons:
            weapon.st *= bonus

    def bonus_aos(self, bonus):
        '''Bonus is 1-based!'''
        for weapon in self.weapons:
            weapon.aos *= bonus

    def additive_to_mt(self, add):
        for weapon in self.weapons:
            weapon.ms += add

GRENADE = Weapon(1, 1, INFANTRY)        # SPECIAL RULE: GRENADES
