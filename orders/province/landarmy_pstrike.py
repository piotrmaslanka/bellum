from __future__ import division
from bellum.province.models import ProvintionalPresence, Reinforcement
from time import time
from datetime import datetime, timedelta
from bellum.landarmy.models import Garrison
from django.core.exceptions import ObjectDoesNotExist
from bellum.orders.models import LandarmyProvintionalStrikeOrder, GenericOrderTable, ProvinceBuildOrder
from bellum.common.fixtures.landarmy_relocate import ppstrikelen
from bellum.common.alliance import isAllied
from bellum.landarmy.decider import whatToDo
from bellum.stats.reports import makeReport, sendTo
from bellum.stats.reports.codebase import WarfareReport
from bellum.orders import DontRemoveGOT
from bellum.stats.larf.const import LX_PROVINCE_COMBAT_LAND
from bellum.stats.larf import note
from bellum.landarmy.defcon.engine import perform, prepare, cleanup

def orderProvintionalStrike(garrison, src_prov, dst_prov, designation, orders, race=None):
    pugs = src_prov.presence.garrison
    pugs -= garrison
    pugs.save()

    garrison.save()
    
    willFinish = datetime.fromtimestamp(int(ppstrikelen(src_prov, dst_prov, garrison, orders, race=race) + time()))
    got = GenericOrderTable(None,
                            willFinish,
                            datetime.now(),
                            7)    
    got.save()
    
    lpso = LandarmyProvintionalStrikeOrder(None,
                                           got.id,
                                           src_prov.presence.owner.id,
                                           src_prov.id,
                                           dst_prov.id,
                                           garrison.id,
                                           designation,
                                           orders)
    lpso.save()    
    
ace = 0

def doLandarmyProvintionalStrikeOrder(entry, lpso=None):
    '''
        If order was to reinforce, signal Exception
    '''

    if lpso == None: lpso = LandarmyProvintionalStrikeOrder.objects.get(got=entry)

    wtd = whatToDo(lpso.attacker, lpso.dstprovince, lpso.designation)

    if wtd == 'REINFORCE':
        if lpso.attacker == lpso.dstprovince.presence.owner:      # Reinforce own province
            lpso.dstprovince.presence.garrison  # make sure it's ready
            lpso.dstprovince.presence.garrison += lpso.garrison
            lpso.garrison.delete()
            lpso.dstprovince.presence.garrison.save()
            lpso.delete()
            return
        try:
            reinforcement = lpso.dstprovince.presence.reinforcement_set.get(owner=lpso.attacker)
        except: # Was not previously reinforced, need to make new classes
            Reinforcement(None, lpso.attacker.id, lpso.dstprovince.presence.id, lpso.garrison.id, lpso.orders).save()
            lpso.delete()
            return
        else:   # Reinforce already reinforced troops
            reinforcement.garrison += lpso.garrison
            reinforcement.garrison.save()
            lpso.garrison.delete()
            lpso.delete()
            return
    elif wtd == 'FALLBACK':
        lpso.directiveFallback(0)
        raise DontRemoveGOT
    elif wtd == 'ASSAULT':
        try:
            lpso.dstprovince.presence             # If uninhabited?
        except:
            pres = ProvintionalPresence(id=None,
                                        garrison=lpso.garrison,
                                        owner=lpso.attacker,
                                        province=lpso.dstprovince,
                                        garrison_orders=0)
            pres.save()
            lpso.delete()
            return

        # War!
        # lpso.attacker WITH HIS lpso.garrison IS ATTACKING lpso.dstprovince

        report = WarfareReport()
        report.initializeEnvironment(lpso.srcprovince, lpso.dstprovince, datetime.now())
        report.initializeParties(lpso.attacker, lpso.dstprovince.presence.owner)
        attacker_army, defender_army = prepare(lpso)
        attacker_won = perform(attacker_army, defender_army, report)
        cleanup(attacker_army, defender_army, report, attacker_won)

        rep = makeReport(report, u'Raport wojenny z '+lpso.dstprovince.name)
        sendTo(rep, lpso.attacker, False)
        sendTo(rep, lpso.dstprovince.presence.owner, False)
        for reinf in lpso.dstprovince.presence.reinforcement_set.all():
            sendTo(rep, reinf.owner, False)


        note(None, LX_PROVINCE_COMBAT_LAND, attacker_id=lpso.attacker.id,
                                                defender_id=lpso.dstprovince.presence.owner.id,
                                                source_pid=lpso.srcprovince.id,
                                                target_pid=lpso.dstprovince.id,
                                                attacker_won=attacker_won)

        if attacker_won == True:
            defender = lpso.dstprovince.presence.owner

            lpso.dstprovince.presence.unsettle_dueToAssault()

            lpso.dstprovince.presence.garrison.clone(lpso.garrison)
            lpso.dstprovince.presence.garrison.save()
            lpso.dstprovince.presence.owner = lpso.attacker
            lpso.dstprovince.presence.save()
            lpso.garrison.delete()

            # Slay all reinforcement garrisons
            for reinf in lpso.dstprovince.presence.reinforcement_set.all():
                reinf.garrison.delete()
                reinf.delete()                            
                
            from bellum.common.fixtures.resources import recalc
            recalc(defender)
            recalc(lpso.attacker)
        else: # if (attacker_won == False) or (attacker_won == None):
            # Save all reinforcement garrisons, delete if necessary
            for reinf in lpso.dstprovince.presence.reinforcement_set.all():
                if reinf.garrison.isZero():
                    reinf.garrison.delete()
                    reinf.delete()
                else:
                    reinf.garrison.save()

            lpso.dstprovince.presence.garrison.save()
            if attacker_won == False: lpso.garrison.delete()
        if attacker_won == None:  # stalemate
            # pack attackers bags and send him home
            lpso.garrison.save()
            lpso.directiveFallback()
            raise DontRemoveGOT
    
        lpso.delete()