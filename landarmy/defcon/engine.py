from bellum.landarmy.defcon.objects import INFANTRY, ARMOR, SUPPORT, Shot, OUTCOME_ATTACKER_WON, OUTCOME_DEFENDER_WON, OUTCOME_STALEMATE, GRENADE
from bellum.landarmy.defcon.specials import DefensiveDrones, DebrisMaker, WhatAMess, WKM, Markerlights, SuicideExplosion, Tarpit, Grenades, SkipBecauseGrenades, PartyArtillery
from bellum.landarmy.defcon.makers import prepare, cleanup
from random import random, choice

def turn(turn_no, attacker_army, defender_army, attacker_first, report, attacker_shoots=True, defender_shoots=True):
    '''shooting modifiers enables to forbid a party from shooting.
       returns True if battle has been resolved'''

    if attacker_first:
        ofensor = attacker_army
        ofensor_shoots = attacker_shoots
        defensor = defender_army
        defensor_shoots = defender_shoots
    else:
        ofensor = defender_army
        ofensor_shoots = defender_shoots
        defensor = attacker_army
        defensor_shoots = attacker_shoots

    ofensor.nextTurn()
    defensor.nextTurn()

    for type_now_firing in (ARMOR, INFANTRY, SUPPORT):
        for party_now_firing, party_now_fired_at in ((ofensor, defensor), (defensor, ofensor)):
            if not defensor_shoots and (party_now_firing==defensor): continue
            if not ofensor_shoots and (party_now_firing==ofensor): continue
            report.startVolley()
                # this will fire in order: O-A, D-A, O-I, D-I, O-S, D-S
            for armygroup in party_now_firing.groups:
                for uid, unit, aou in armygroup.units[type_now_firing]:
                    for _i in xrange(0, aou):
                        # this is for single unit
                        # ----------- check what can be targeted
                        can_target_armor = party_now_fired_at.isTargetable(ARMOR)
                        can_target_infantry = party_now_fired_at.isTargetable(INFANTRY)

                        if not (can_target_armor or can_target_infantry):   # no unit can be targeted
                            return True         # battle is over
                        # ----------- check some special rules
                        if unit.special(PartyArtillery) != False:                # SPECIAL RULE: PARTY ARTILLERY
                            if random() < 0.8:      #
                                party_now_fired_at.maxdebris -= 3
                            else:
                                if random() < 0.5:          # kill random own
                                    party_now_firing.slayRandom(unit)
                                else:                       # kill random enemy
                                    party_now_fired_at.slayRandom(unit)
                        # ----------- make a tuple called 'weapons_picked' which contains weapons the unit will fire
                        if unit.mt:         # unit has multitracker. It doesn't need to decide on a weapon
                            weapons_picked = unit.weapons
                        else:               # unit doesn't have a multitracker. it must pick a gun
                            pw = unit.pickWeapon(can_target_armor, can_target_infantry, turn_no=turn_no)
                            if pw == None:      # unit could not target anything
                                weapons_picked = ()
                            else:
                                weapons_picked = (pw, )
                        # ---------- check some special rules
                        if unit.special(DefensiveDrones) != False:          # SPECIAL RULE: DEFENSIVE DRONES
                            party_now_firing.defdrones += 1
                        if unit.special(Markerlights) != False:
                            party_now_fired_at.markerlights += unit.special(Markerlights).x
                        # ----------- fire every weapon
                        for weapon in weapons_picked:
                            if weapon.special(WhatAMess):                   # SPECIAL RULE: WHAT A MESS(x)
                                party_now_fired_at.maxdebris += weapon.special(WhatAMess).x
                            weapon_shot = weapon.shot(unit)
                            for __i in xrange(0, int(weapon.aos)):  # fire AOS times
                                didKill, spcRules = party_now_fired_at.receiveFire(weapon_shot)
                                if didKill:
                                    if weapon.special(WKM) != False:            # SPECIAL RULE: WKM
                                        party_now_fired_at.maxdebris -= 1
                                    if Tarpit in spcRules:                      # SPECIAL RULE: TARPIT
                                        break
                                    if weapon.special(SuicideExplosion) != False:  # SPECIAL RULE: SUICIDE EXPLOSION
                                        armygroup._blast(type_now_firing, uid)
                                        party_now_fired_at.maxdebris -= 1       # account for debris that enemy got by
                                                                        # having his armor die in hands of SUICIDE EXPLODER
                                    if weapon.special(Grenades) != False:            # SPECIAL RULE: GRENADES
                                        if not (SkipBecauseGrenades in spcRules):   # if killing this unit could fire up grenades..
                                            for ___i in xrange(0, weapon.special(Grenades).x):                                                
                                                party_now_fired_at.receiveFire(GRENADE.shot(unit), canUseDebris=False, canUseMarkerlights=False)
            report.endVolley()
    return False

def perform(attacker_army, defender_army, report, is_drop=False):
    report.initializeArmies(attacker_army, defender_army, is_drop=is_drop)
    report.startBattle()
    turn_no = 0
    if is_drop:
        report.startTurn(drop=True)
        if turn(turn_no, attacker_army, defender_army, False, report, attacker_shoots=False):
            report.endTurn()
            report.endBattle()
            report.definitiveVictory()
            if attacker_army.isTargetable():
                return OUTCOME_ATTACKER_WON
            else:
                return OUTCOME_DEFENDER_WON
        report.endVolley()
        report.endTurn()

    auc = attacker_army.countAllUnits(), defender_army.countAllUnits()
    momentum = 5

    attacker_first = True

    while True:
        turn_no += 1
        report.startTurn()
        tr = turn(turn_no, attacker_army, defender_army, attacker_first, report)
        report.endTurn()
        if tr:
            report.endBattle()
            report.definitiveVictory()
            if attacker_army.isTargetable():
                return OUTCOME_ATTACKER_WON
            else:
                return OUTCOME_DEFENDER_WON
        # Do a momentum check
        _auc = attacker_army.countAllUnits(), defender_army.countAllUnits()
        if auc == _auc:
            momentum -= 1
            if momentum == 0:
                report.momentumLost()
                report.endBattle()
                return OUTCOME_STALEMATE
        else:
            auc = _auc
            momentum = 5

        attacker_first = not attacker_first