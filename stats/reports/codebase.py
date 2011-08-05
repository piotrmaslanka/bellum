# coding=UTF-8
from bellum.mother.models import Mother
from bellum.landarmy.defcon.report import Report
from bellum.alliance.models import AllianceMembership
from bellum.common.fixtures.landarmy_stats import UNIT_NAMES
from bellum.landarmy.defcon.objects import INFANTRY, ARMOR, SUPPORT
from datetime import datetime

class BaseReport(object):
    pass

class Participant(object):
    def __init__(self, accountObject, require_alliance=False):
        self.empire = accountObject.empire
        self.id = accountObject.id
        self.race = accountObject.race

        if require_alliance:
            try:
                am = AllianceMembership.objects.get(account=accountObject)
            except:
                self.alliance_shname = None
                self.alliance_id = None
            else:
                self.alliance_shname = am.alliance.shname
                self.alliance_id = am.alliance.id

class Planet(object):
    def __init__(self, planetObject):
        self.name = planetObject.name
        self.id = planetObject.id

class ProvinceOrMother(object):
    def __init__(self, obj):
        self.name = obj.name
        self.id = obj.id
        self.isMother = isinstance(obj, Mother)
        self.isProvince = not self.isMother

class RadarReportv01(BaseReport):
    def __init__(self, fprov, rlevel):
        super(RadarReportv01, self).__init__()
        self.mothers = []
        self.rlevel = rlevel
        self.minbound = []
        self.moutbound = []
        self.province = ProvinceOrMother(fprov)
    def appendStationary(self, mObject):
            # 0 - Stationary
            # 1 - Outbound
            # 2 - Inbound
        self.mothers.append((Participant(mObject.owner), ProvinceOrMother(mObject), None))
    def appendInbound(self, mro):
        self.minbound.append((Participant(mro.mother.owner), ProvinceOrMother(mro.mother), Planet(mro.loc_from)))
    def appendOutbound(self, mro):
        self.moutbound.append((Participant(mro.mother.owner), ProvinceOrMother(mro.mother), Planet(mro.loc_to)))

class ScanReportv01(BaseReport):
    def __init__(self):
        super(ScanReportv01, self).__init__()
        self.code = {'troops':[], 'owner':None, 'province':None, 'buildings':None}
        self.setResourceCoefficients(None, None, None)
        self.setNaturalDefenseLevel(None)
    def _ainn(self, name, value):
        self.code[name] = value
    def setResourceCoefficients(self, town_coef, titan_coef, pluton_coef):
        self._ainn('town_coef', town_coef)
        self._ainn('titan_coef', titan_coef)
        self._ainn('pluton_coef', pluton_coef)
    def setNaturalDefenseLevel(self, natural_defense_level):
        self._ainn('natural_defense_level', natural_defense_level)
    def setBuildings(self, p):
        b = {}
        for i in xrange(0, p.province.slots):
            b[i] = p.getPair(i)
        self._ainn('buildings',b)
    def setOwner(self, participant):
        self._ainn('owner', Participant(participant))
    def setProvince(self, province):
        self._ainn('province', ProvinceOrMother(province))
    def setGarrison(self, owner, garrison):
        from bellum.landarmy.models import cloneGarrison
        self.code['troops'].append((Participant(owner), cloneGarrison(garrison)))
    def setFree(self, free):
        self.code['free'] = free

class WarfareReport(BaseReport, Report):
    '''@happened_on [datetime] when happened (datetime)
       @destination [Province] where happened
       @source [Province/Mother] source of attack
    '''

    def __init__(self):
        super(WarfareReport, self).__init__()

        # main meat
    def startTurn(self, drop=False):
        try:
            self.ctid
        except:
            if drop:
                self.ctid = 0
            else:
                self.ctid = 1
        else:
            self.ctid += 1
        # Important abstraction!!!
        # U-Lists
            # ulist position = list( seq(account_id, empire_name)),
            #                        seq(...   tuple(unit count, unit name)) ...))

        # do attacker turn
        ua = []
        for aag in self._army_a.groups:        # aag - Attacker Army Group
            uau = [(aag.owner.id, aag.owner.empire)]
            uaul = []
            for utype in (INFANTRY, ARMOR, SUPPORT):
                for uid, unit, cnt in aag.units[utype]:
                    uaul.append((cnt, UNIT_NAMES[aag.owner.race][uid]))
            uau.append(uaul)
            ua.append(uau)
        # do defender turn

        ud = []
        for dag in self._army_d.groups:        # dag - Defender Army Group
            udu = [(dag.owner.id, dag.owner.empire)]
            udul = []
            for utype in (INFANTRY, ARMOR, SUPPORT):
                for uid, unit, cnt in dag.units[utype]:
                    udul.append((cnt, UNIT_NAMES[dag.owner.race][uid]))
            udu.append(udul)
            ud.append(udu)
            
        # single turn entry     -       seq(turn_id, attacker_debris, defender_debris, attacker_U, defender_U)
        self.turns.append((self.ctid, self._army_a.maxdebris, self._army_d.maxdebris, ua, ud))

        # useless
    def endTurn(self): pass
    def startVolley(self, is_drop=False): pass
    def endVolley(self): pass
        # single invocation initializers
    def startBattle(self):
        self.turns = []
    def endBattle(self):
        self.startTurn()        # just for the sake of it
        self.endTurn()
        del self._army_a
        del self._army_d
    def finalize(self, report):
        self.attacker_won = report
    def momentumLost(self):
        self.resolved = False
    def definitiveVictory(self):
        self.resolved = True
    def initializeEnvironment(self, source, destination, occurred_on):
        self.happened_on = occurred_on
        self.destination = ProvinceOrMother(destination)
        self.source = ProvinceOrMother(source)
    def initializeParties(self, attacker, root_defender):
        self.attacker = Participant(attacker, require_alliance=True)
        self.defender = Participant(root_defender, require_alliance=True)
    def initializeArmies(self, attacker_army, defender_army, is_drop):
        self._army_a = attacker_army
        self._army_d = defender_army


