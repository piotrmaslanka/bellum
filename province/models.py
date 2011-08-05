from django.db import models
from bellum.common.models import XYPosition
from bellum.register.models import Account
from bellum.mother.models import Planet 
from django.core.exceptions import ObjectDoesNotExist
from bellum.landarmy.models import Garrison, ArmyOrder    

class Province(XYPosition):
    planet_count_number = models.PositiveSmallIntegerField()
        # number of the province on the planet. Starts from zero.
    name = models.CharField(max_length=35)

    town_coef = models.FloatField()
    titan_coef = models.FloatField()
    pluton_coef = models.FloatField()

    slots = models.PositiveSmallIntegerField()

    natural_defense_level = models.FloatField()
    planet = models.ForeignKey(Planet)

    def getNeighbours(self):
        neighbours = ()
        for x in xrange(0, self.planet.amount_of_provinces):
            if x==self.planet_count_number:
                continue
            if self.planet.isLink(self.planet_count_number, x):
                neighbours += (x, )
        return Province.objects.filter(planet=self.planet).filter(planet_count_number__in=neighbours)

    def isOccupied(self):
        '''Returns True on province occupied, returns False on province clear'''
        try:
            self.provintionalpresence
        except ObjectDoesNotExist:
            return False
        return True
    
    def __getPresence__(self):
        try:
            if self.CACHEDPRESENCE == None:
                raise ObjectDoesNotExist
            else:
                return self.CACHEDPRESENCE
        except AttributeError:
            try:
                self.CACHEDPRESENCE = self.provintionalpresence_set.get(province=self)
            except ObjectDoesNotExist:
                self.CACHEDPRESENCE = None
            return self.__getPresence__()

    def __getattr__(self, name):
        '''Used to implement presence alias for my ProvintionalPresence item'''
        if name=='presence':
            return self.__getPresence__()
        elif name=='provintionalpresence':
            return self.__getPresence__()
        else:
            raise AttributeError, 'Not found '+name+' in stuffz'
        
    def __unicode__(self):
        return unicode(self.name)
        
class ProvintionalPresence(models.Model):
    owner = models.ForeignKey(Account)
    province = models.ForeignKey(Province)
    s0type = models.PositiveSmallIntegerField(default=0)
    s1type = models.PositiveSmallIntegerField(default=0)
    s2type = models.PositiveSmallIntegerField(default=0)
    s3type = models.PositiveSmallIntegerField(default=0)
    s4type = models.PositiveSmallIntegerField(default=0)
    s0lvl = models.PositiveSmallIntegerField(default=0)
    s1lvl = models.PositiveSmallIntegerField(default=0)
    s2lvl = models.PositiveSmallIntegerField(default=0)
    s3lvl = models.PositiveSmallIntegerField(default=0)
    s4lvl = models.PositiveSmallIntegerField(default=0)
    
    garrison = models.ForeignKey(Garrison)
    garrison_orders = ArmyOrder()


    def getPair(self, id):
        return (self.__dict__['s'+str(id)+'type'], self.__dict__['s'+str(id)+'lvl'])
    def setPair(self, id, type, lvl):
        self.__dict__['s'+str(id)+'type'] = type
        self.__dict__['s'+str(id)+'lvl'] = lvl


    def getPendingBuildingsCount(self):
        from bellum.orders.models import ProvinceBuildOrder
        return ProvinceBuildOrder.objects.filter(ppresence=self).count()
    def getPendingBuilds(self):
        from bellum.orders.models import ProvinceBuildOrder
        return ProvinceBuildOrder.objects.filter(ppresence=self)
    def getBuildObject(self, slot):
        from bellum.orders.models import ProvinceBuildOrder
        return ProvinceBuildOrder.objects.get(ppresence=self, slot=slot)

    def _fallback_armies(self):
        '''Makes every army which is going designation 0 to this province to go to source province with designation 1.
           Does save'''
        from bellum.orders.models import LandarmyProvintionalStrikeOrder, LandarmyPlanetaryStrikeOrder

        lpsos = LandarmyProvintionalStrikeOrder.objects.filter(dstprovince=self.province).filter(designation=0)

        for lpso in lpsos:
            lpso.directiveFallback()

    def _cancel_actions(self):
        from bellum.orders.models import GenericOrderTable, ProvinceBuildOrder

        pb = ProvinceBuildOrder.objects.filter(ppresence=self)
        for p in pb:
            p.got.delete()
            p.delete()

    def unsettle(self):
        '''Does not save
        Cancels building actions and resets buildings.
        Invoke on abandoning province'''
        self._cancel_actions()
        self._fallback_armies()
        self.setPair(0, 0, 0)
        self.setPair(1, 0, 0)
        self.setPair(2, 0, 0)
        self.setPair(3, 0, 0)
        self.setPair(4, 0, 0)
        
    def unsettle_dueToAssault(self):
        '''Invoke when a province is forcibly taken, so that buildings don't get destroyed'''
        self._cancel_actions()

class Reinforcement(models.Model):
    owner = models.ForeignKey(Account)
    presence = models.ForeignKey(ProvintionalPresence)
    garrison = models.ForeignKey(Garrison)
    garrison_orders = ArmyOrder()