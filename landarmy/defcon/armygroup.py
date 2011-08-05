from bellum.meta import MGID
from bellum.landarmy.defcon.objects import INFANTRY, ARMOR, SUPPORT, MULTIATTACK
from bellum.landarmy.defcon.specials import Tarpit
from copy import deepcopy
from random import uniform

class ArmyGroup(object):
    '''An army belonging to a single player'''
    def isTargetable(self, utype=None):
        '''army group is not targetable when only living units are support.
        when type is specified, will return whether units of given type are targetable'''
        if utype == None:
            return (self.aou[INFANTRY] != 0) or (self.aou[ARMOR] != 0)
        else:
            return self.aou[utype] > 0

    def nextTurn(self): pass

    def countAllUnits(self): return self.aou[INFANTRY] + self.aou[ARMOR] + self.aou[SUPPORT]

    def countUnits(self, utype):
        '''if utype == None then counts all units that may be targeted'''
        if utype == MULTIATTACK:
            return self.aou[INFANTRY] + self.aou[ARMOR]
        else:
            return self.aou[utype]

    def _blast(self, utype, uid):
        '''just removes an unit from table. nothing else. Uid is unique type, not array identifier'''
        uindice = -1
        for uuid, unit, cnt in self.units[utype]:
            uindice += 1
            if uuid==uid:
                break
        if uindice == -1: raise Exception, 'Did not found!'
        self.units[utype][uindice][2] -= 1      # decrement unit
        if self.units[utype][uindice][2] == 0:      # if all units of given type were killed
            del self.units[utype][uindice]      # remove them

    def __choice(self, utype):
        '''picks a random unit from given unittype with chances proportional to its amount.
           returns it's self.units[utype] seq indice
           unittype MUST BE INFANTRY or ARMOR'''
        total_prob = self.aou[utype]
        chosen = uniform(0, total_prob)
        cumulative = 0
        indice = 0
        for id, unit, amount in self.units[utype]:
            cumulative += amount
            if cumulative > chosen:
                return indice
            indice += 1

    def receiveFire(self, shot, army, canUseDebris=True, canUseMarkerlights=True):
        '''@army parent army object. Receive a shot. Perform needed modifications. Returns a cool tuple'''
        assert shot.type in (ARMOR, INFANTRY), 'Invalid shot type '+str(shot.type)
        uindice = self.__choice(shot.type)
        unit = self.units[shot.type][uindice][1]
        wasHit = unit.receiveFire(shot, army, canUseDebris=canUseDebris, canUseMarkerlights=canUseMarkerlights)

        if wasHit:
            self.units[shot.type][uindice][2] -= 1      # decrement unit
            if self.units[shot.type][uindice][2] == 0:      # if all units of given type were killed
                del self.units[shot.type][uindice]      # remove them

            if shot.type == ARMOR:      # we killed an armoured unit
                army.maxdebris += 1
                army.debris += 1

            self.aou[shot.type] -= 1        # decrement units of given type

            if unit.special(Tarpit) != False:                   # SPECIAL RULE: TARPIT
                return (True, (Tarpit, ))


        return (wasHit, ())

    def targetUnit(self, shotObject, specialRules=None):
        '''Target one of my units with shotObject and optional specialRules seq of objects.
           Returns a tuple (unit type, unit id, unit object, amount of units).'''
        # now we should target a unit
        total_prob = self.aou[shotObject.type]
        chosen = uniform(0, total_prob)
        cumulative = 0
        for id, definition, amount in self.units[shotObject.type]:
            cumulative += amount
            if cumulative > chosen:
                return (shotObject.type, id, definition, amount)

    def writeback(self):
        '''write surviving units to rootGarrisonObject. Does not save'''
        for i in xrange(0, MGID+1):
            self.rootGarrisonObject[i] = 0
        for uclass in self.units:
            for u in uclass:
                if u[0] == None:
                    continue
                self.rootGarrisonObject[u[0]] = u[2]

    def __init__(self, rootGarrisonObject, owner, is_offense):
        '''this just generates an army group. It does not apply bonuses.
           true if this party acts in offense'''
        from bellum.common.fixtures.landarmy_stats import UNIT_STATS
        agh = UNIT_STATS[owner.race][{True:0, False:1}[is_offense]]

        self.owner = owner
        self.rootGarrisonObject = rootGarrisonObject
        self.units = [[], [], []]
        self.aou = [0, 0, 0]

        for i in xrange(0, MGID+1):
            if rootGarrisonObject[i] > 0:
                            # we need it copied along with all of its weapon, so we use deepcopy
                            # append a list(unit id, Unit object, amount of units)
                self.units[agh[i].type].append([i, deepcopy(agh[i]), rootGarrisonObject[i]])
                self.aou[agh[i].type] += rootGarrisonObject[i]

                        # sort by initiative
        for cat in (INFANTRY, ARMOR, SUPPORT): self.units[cat].sort(key=lambda x: x[1].initiative, reverse=True)

    def bonus_im(self, bonus):
        for id, iunit, cnt in self.units[INFANTRY]:
            iunit.bonus_im(bonus)

    def bonus_to_ctinfantry(self, bonus):
        for id, iunit, cnt in self.units[INFANTRY]:
            iunit.bonus_ct(bonus)
            
    def bonus_to_ctarmor(self, bonus):
        for id, aunit, cnt in self.units[ARMOR]:
            aunit.bonus_ct(bonus)

    def bonus_to_ct(self, bonus):
        self.bonus_to_ctinfantry(bonus)
        self.bonus_to_ctarmor(bonus)

    def bonus_to_st(self, bonus, support=False):
        for id, iunit, cnt in self.units[INFANTRY]:
            iunit.bonus_st(bonus)
        for id, aunit, cnt in self.units[ARMOR]:
            aunit.bonus_st(bonus)
        if support: self.bonus_to_st_support(bonus)

    def bonus_to_st_support(self, bonus):
        for id, sunit, cnt in self.units[SUPPORT]:
            sunit.bonus_st(bonus)

    def bonus_to_aos_support(self, bonus):
        for id, sunit, cnt in self.units[SUPPORT]:
            sunit.bonus_aos(bonus)

    def additive_to_mt(self, add):
        '''adds to ALL UNITS!!!'''
        for units in self.units:
            for id, sunit, cnt in units:
                sunit.additive_to_mt(add)