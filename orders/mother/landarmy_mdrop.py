from __future__ import division
from bellum.orders.models import LandarmyPlanetaryStrikeOrder, GenericOrderTable, ProvinceBuildOrder
from bellum.province.models import ProvintionalPresence, Reinforcement
from time import time
from datetime import datetime, timedelta
from bellum.landarmy.models import Garrison
from django.core.exceptions import ObjectDoesNotExist
from bellum.common.fixtures.landarmy_relocate import mpstrikelen
from bellum.landarmy.decider import whatToDo
from bellum.stats.reports import makeReport, sendTo
from bellum.stats.larf.const import LX_DROP_COMBAT_LAND
from bellum.stats.larf import note
from bellum.orders import DontRemoveGOT
from bellum.orders.models import LandarmyMotherPickupOrder
from bellum.common.fixtures.landarmy_relocate import pmmovelen
from time import time
from bellum.stats.reports.codebase import WarfareReport
from bellum.landarmy.defcon.engine import perform, prepare, cleanup

def orderPlanetaryStrike(garrison, mother, province, designation, orders, race=None):
    mother.garrison -= garrison
    mother.garrison.save()
    garrison.save()
    
    willFinish = datetime.fromtimestamp(int(mpstrikelen(mother, province, garrison, orders, race=race) + time()))
    got = GenericOrderTable(None,
                            willFinish,
                            datetime.now(),
                            6)    
    got.save()
    
    lpso = LandarmyPlanetaryStrikeOrder(None,
                                       got.id,
                                       mother.id,
                                       province.id,
                                       garrison.id,
                                       designation,
                                       orders)
    lpso.save()


def doLandarmyPlanetaryStrikeOrder(entry):
    '''
        If order was to reinforce, signal Exception
    '''
    lpso = LandarmyPlanetaryStrikeOrder.objects.get(got=entry)

    wtd = whatToDo(lpso.mother.owner, lpso.province, lpso.designation)

    if wtd == 'REINFORCE':
        if lpso.mother.owner == lpso.province.presence.owner:      # Reinforce own province
            lpso.province.presence.garrison += lpso.garrison
            lpso.province.presence.garrison.save()
            lpso.garrison.delete()
            lpso.delete()
            return
                                                             # Reinforce somebody's else province
        try:
            reinforcement = lpso.province.presence.reinforcement_set.get(owner=lpso.mother.owner)
        except:                          # I have no reinforcements in this province
            Reinforcement(None, lpso.mother.owner.id, lpso.province.presence.id, lpso.garrison.id, lpso.orders).save()
            lpso.delete()
            return
        else:                            # I do have reinforcements on this province
            reinforcement.garrison += lpso.garrison
            reinforcement.garrison.save()
            lpso.garrison.delete()
            lpso.delete()
            return
    elif wtd == 'FALLBACK':
        lmpo = LandarmyMotherPickupOrder(None, lpso.got.id, lpso.mother.id, lpso.province.id, lpso.garrison.id)
        lmpo.save()
        lpso.got.ordertype = 8
        lpso.got.to_be_completed += timedelta(0, int(pmmovelen(lpso.province, lpso.mother, lpso.garrison)))
        lpso.got.save()
        lpso.delete()
        raise DontRemoveGOT
    elif wtd == 'ASSAULT':
        try:
            lpso.province.presence          # If uninhabited?
        except:
            pres = ProvintionalPresence(id=None,
                                        garrison=lpso.garrison,
                                        owner=lpso.mother.owner,
                                        province=lpso.province,
                                        garrison_orders=lpso.orders)
            pres.save()
            lpso.delete()
            return

        report = WarfareReport()
        report.initializeEnvironment(lpso.mother, lpso.province, datetime.now())
        report.initializeParties(lpso.mother.owner, lpso.province.presence.owner)
        attacker_army, defender_army = prepare(lpso)
        attacker_won = perform(attacker_army, defender_army, report, is_drop=True)
        cleanup(attacker_army, defender_army, report, attacker_won)

        rep = makeReport(report, u'Raport wojenny z '+lpso.province.name)
        sendTo(rep, lpso.mother.owner, False)
        sendTo(rep, lpso.province.presence.owner, False)
        for reinf in lpso.province.presence.reinforcement_set.all():
            sendTo(rep, reinf.owner, False)

        note(None, LX_DROP_COMBAT_LAND, attacker_id=lpso.mother.owner,
                                        defender_id=lpso.province.presence.owner,
                                        province_id=lpso.province,
                                        attacker_won=attacker_won)

        if attacker_won:
            defender = lpso.province.presence.owner
                    # Elliminate all reinforcements
            reinfs = Reinforcement.objects.filter(presence=lpso.province.presence)
            for reinf in reinfs:
                reinf.garrison.delete()
                reinf.delete()

            lpso.province.presence.unsettle_dueToAssault()

            lpso.province.presence.garrison.clone(lpso.garrison)# Copy to presence's garrison info about garrison
            lpso.province.presence.garrison.save()

            lpso.province.presence.owner = lpso.mother.owner  # Change owner
            lpso.province.presence.save()

            lpso.garrison.delete()

            from bellum.common.fixtures.resources import recalc
            recalc(defender)
            recalc(lpso.mother.owner)
        if attacker_won in (False, None):       # save garrisons
            # Save all reinforcement garrisons, delete if necessary
            for reinf in lpso.province.presence.reinforcement_set.all():
                if reinf.garrison.isZero():
                    reinf.garrison.delete()
                    reinf.delete()
                else:
                    reinf.garrison.save()

            lpso.province.presence.garrison.save()
            if attacker_won == False: lpso.garrison.delete()
        if attacker_won == None:
            lpso.garrison.save()
            lpso.fallback()
            raise DontRemoveGOT

        lpso.delete()    