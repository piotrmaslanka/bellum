from bellum.landarmy.defcon.objects import INFANTRY, ARMOR, SUPPORT, MULTIATTACK, Unit, Weapon
from math import pow
from bellum.meta import MSI
from bellum.landarmy.defcon.specials import SkipBecauseGrenades, DebrisMaker
from bellum.landarmy.defcon.dmath import provintionalpresence_to_im
from random import uniform, random

class Army(object):
    def __init__(self, *armygroups):
        self.groups = armygroups
        self.maxdebris = 0
        self.debris = 0
        self.defdrones = 0                       # SPECIAL RULE: DEFENSIVE DRONES
        self.markerlights = 0

        for group in self.groups:           # SPECIAL RULE: DEBRIS MAKER
            for unitg in group.units:           # preliminary count of debris thanks to DEBRIS MAKER
                for uid, unit, cnt in unitg:
                    if unit.special(DebrisMaker) != False:
                        self.maxdebris += unit.special(DebrisMaker).x * cnt

    def countAllUnits(self):
        units = 0
        for group in self.groups: units += group.countAllUnits()
        return units

    def writeback(self):
        for group in self.groups: group.writeback()

    def nextTurn(self):
        '''Called on new turn'''
        self.debris = int(self.maxdebris)
        if self.debris < 0: self.debris = 0
        for group in self.groups: group.nextTurn()

    def isTargetable(self, utype=None):
        '''returns whether an army is alive. if type is specified, then returns whether given unit type
           is targetable'''
        for armygroup in self.groups:
            if armygroup.isTargetable(utype): return True
        return False

    def applyFortifications(self, presence):
        '''applies fortifications to debris points
           returns added debris points'''
        units = 0
        for armygroup in self.groups:
            for unitclass in armygroup.units[INFANTRY]:
                units += unitclass[2]
                
        forts = 0
        for i in xrange(0, MSI+1):
            stype, slvl = presence.getPair(i)
            if stype == 5: forts += slvl

        coef = (pow(1.05, forts)-1)*units
        self.maxdebris += coef
        return coef

    def applyBuildingCount(self, presence):
        '''apply Im bonus from amount of buildings on province'''
        im = provintionalpresence_to_im(presence)
        for armygroup in self.groups:
            armygroup.bonus_im(im)

    def applyPm(self, province):
        '''should be applied only to attacking forces, as it is a potentially negatory bonus'''
        bonus = pow(0.9, province.natural_defense_level-1)
        for group in self.groups:
            group.bonus_to_st(bonus, support=True)

    def slayRandom(self, slayer):
        '''slayer is a Unit'''
        can_target_armor = self.isTargetable(ARMOR)
        can_target_infantry = self.isTargetable(INFANTRY)

        if can_target_armor and can_target_infantry:
            if random() <= 0.5:
                self.receiveFire(Weapon(1, 1, INFANTRY).shot(slayer), canUseDebris=False, canUseMarkerlights=False, canUseDrones=False)
            else:
                self.receiveFire(Weapon(1, 1, ARMOR).shot(slayer), canUseDebris=False, canUseMarkerlights=False, canUseDrones=False)
        elif can_target_armor:
                self.receiveFire(Weapon(1, 1, ARMOR).shot(slayer), canUseDebris=False, canUseMarkerlights=False, canUseDrones=False)
        elif can_target_infantry:
                self.receiveFire(Weapon(1, 1, INFANTRY).shot(slayer), canUseDebris=False, canUseMarkerlights=False, canUseDrones=False)              


    def receiveFire(self, shot, canUseDebris=True, canUseMarkerlights=True, canUseDrones=True):
        '''@shot bellum.landarmy.defcon.objects.Shot'''
        # will a drone take the shot?
        if canUseDrones and (self.defdrones > 0):                  # ----------------- SPECIAL RULE: DEFENSIVE DRONES
            drone = Unit(1, 1, 0, shot.type, False, ())
            if drone.receiveFire(shot, self, canUseDebris=False): self.defdrones -= 1
            return (False, (SkipBecauseGrenades, ))
        # first we need to decide what army group are we going to shoot at
            # get count of units of given type in a group and group
        agd = map(lambda x: (x.countUnits(shot.type), x), self.groups)
            # filter groups that are untargetable
        agd = filter(lambda x: x[0] > 0, agd)
        total_prob = 0
        for amount, group in agd: total_prob += amount
        chosen = uniform(0, total_prob)
        cumulative = 0
        for amount, group in agd:
            cumulative += amount
            if cumulative > chosen:
                break
        # group is the army group that will receive fire
        try:
            group
        except:
                # You mean this shouldn't appear here? I'm gonna tell you why.
                # If we are shooting a multi-AOS gun, then we don't check what can be targeted and what can't
                # between shots, because it would take a crapload of time
                # that's why some times we have a shot that's unroutable here. We need to account for it and dismiss it.
            return (False, ())

        return group.receiveFire(shot, army=self, canUseDebris=canUseDebris, canUseMarkerlights=canUseMarkerlights)
