# coding=UTF-8
from bellum.stats.reports.codebase import ScanReportv01
from bellum.stats.reports import makeReport, sendTo
from bellum.common.models import ResourceIndex
from bellum.province.models import Province
from random import choice
from bellum.stats.igstatistics.resources_sent import note

def doScan(account, mother, province):
    '''Exception on failure. Will use Exceptions unicode() to generate error message in HTML.
    Returns a report'''
    attacker_spy_level = account.technology.o_13        # Racial tech, attacker is always Magnuss

#    if ResourceIndex(titan=5000, pluton=2000, men=50) >= mother.owner.resources.stateUpdate():
#        raise ScanException(u'Nie stać cię! Skan wymaga 5000 tytanu, 2000 plutonu i 50 manpower!')

#    mother.owner.resources -= ResourceIndex(titan=5000, pluton=2000, men=50)
#    mother.owner.resources.save()
#    note(mother.owner.id, ResourceIndex(titan=5000, pluton=2000, men=50), 'scans')


    rep = ScanReportv01()
    rep.setProvince(province)

    try:
        province.presence
    except:
        rep.setFree(True)
        gamma = attacker_spy_level + choice((-1, 0, 1))
        if gamma > 4:
            rep.setResourceCoefficients(province.town_coef, province.titan_coef, province.pluton_coef)

    else:
        rep.setFree(False)

        if province.presence.owner == account:
            # If scanning self!
            attacker_spy_level = 10000
            defender_counterspy_level = 0

        defender_counterspy_level = province.presence.owner.technology.o_5
        gamma = attacker_spy_level - defender_counterspy_level + choice((-1, 0, 1))

        if gamma > -65535:
            rep.setOwner(province.presence.owner)
        if gamma > -3:
            rep.setNaturalDefenseLevel(province.natural_defense_level)
        if gamma > -1:
            rep.setBuildings(province.presence)
        if gamma > 1:
            rep.setGarrison(province.presence.owner, province.presence.garrison)
        if gamma > 3:
            for reinf in province.presence.reinforcement_set.all():
                rep.setGarrison(reinf.owner, reinf.garrison)
        if gamma > 4:
            rep.setResourceCoefficients(province.town_coef, province.titan_coef, province.pluton_coef)

    mrp = makeReport(rep, 'Raport szpiegowski z '+province.name)
    sendTo(mrp, account, True)
