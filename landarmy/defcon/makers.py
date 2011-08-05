'''This module generates army groups with applied technology bonuses'''

from bellum.landarmy.defcon.armygroup import ArmyGroup
from bellum.landarmy.defcon.army import Army
from bellum.landarmy.defcon.objects import INFANTRY, ARMOR, SUPPORT
from math import pow

def mk_armygroup(garrisonObject, owner, technology, is_offense):
    ag = ArmyGroup(garrisonObject, owner, is_offense)
    # now we should update SMa and SMo
            
    ag.bonus_to_ctinfantry(pow(1.05, technology.o_0))       # o_0: Infantry Armor   : 2%
    ag.bonus_to_ct(pow(1.05, technology.o_1))               # o_1: Nanobot Armor    : 5%
    ag.bonus_to_ctarmor(pow(1.02, technology.o_8))          # o_8: Tank Armor       : 2%
    ag.bonus_to_st(pow(1.05, technology.o_7))               # o_7: Offensive Systems: 2%
    ag.bonus_to_st_support(pow(1.02, technology.o_9))       # o_9: Support          : 2%

    ag.additive_to_mt(0.01*technology.o_6)                  # o_6: Optotechnics     : 0.01 to MT

    if owner.race == 0:       # Party
        ag.bonus_to_st(pow(1.05, technology.o_13))           # o_13: Racial          : 5%

    if (not is_offense) and (owner.race == 2):
        ag.additive_to_mt(0.01*technology.o_13)             # o_13: Racial          : 0.01 to MT in defense

    # now we should update, in order, Im, Pm and fortifications. But we are done here
    return ag

def prepare(pso):
        '''pso is a provintionalstrike order or planetarystrike order.
           it prepares and returns a tuple of Army instances - attacker and defender'''
        try:
            province = pso.dstprovince
            isDrop = False
        except:
            province = pso.province
            isDrop = True

        # first the assailant ------------------------------------
        if isDrop: attacker = Army(mk_armygroup(pso.garrison, pso.mother.owner, pso.mother.owner.technology, True))
        else:      attacker = Army(mk_armygroup(pso.garrison, pso.attacker, pso.attacker.technology, True))

        # now apply Im and Pm
        attacker.applyBuildingCount(province.presence)
        attacker.applyPm(province)

        # now the defending party --------------------------------
        # now the main defender
        defgroups = [mk_armygroup(province.presence.garrison, province.presence.owner, province.presence.owner.technology, False)]
        # and reinforcements

        debris_prescaler = 0            # together Technocrat racial level

        for reinf in province.presence.reinforcement_set.all():
            defgroups.append(mk_armygroup(reinf.garrison, reinf.owner, reinf.owner.technology, False))
            if reinf.owner.race == 2:       # if Technocrat
                debris_prescaler += reinf.owner.technology.o_13

        defender = Army(*defgroups)

        defender.applyBuildingCount(province.presence)
        defender.applyFortifications(province.presence)

        defender.maxdebris *= pow(1.05, debris_prescaler)

        # ok, here we have a attacker and defender armies and we are ready to fight
        return attacker, defender

def cleanup(attacker_army, defender_army, report, result):
    attacker_army.writeback()
    defender_army.writeback()
    report.finalize(result)
    