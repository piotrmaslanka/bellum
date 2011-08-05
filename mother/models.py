# coding=UTF-8
from django.db import models
from django import forms
from bellum.space.models import Planet
from bellum.register.models import Account
from bellum.common.models import ResourceIndex   
from bellum.landarmy.models import Garrison, ArmyOrder    
from django.core.exceptions import ObjectDoesNotExist

class Mother(models.Model):
    '''Mothership model
    kustomization is fer dem orky grafyyks.
    At the beginning engine wont be able to fly, so level 0 lol'''
    name = models.CharField(max_length=20, blank=False, null=False)
    b_0 = models.PositiveIntegerField(default=0)     # engine
    b_1 = models.PositiveIntegerField(default=0)     # quarters
    b_2 = models.PositiveIntegerField(default=0)     # dust collector
    b_3 = models.PositiveIntegerField(default=0)     # armory
    b_4 = models.PositiveIntegerField(default=0)     # lab
    b_5 = models.PositiveIntegerField(default=0)     # hangar
    b_6 = models.PositiveIntegerField(default=0)
    b_7 = models.PositiveIntegerField(default=0)
    b_8 = models.PositiveIntegerField(default=0)
    b_9 = models.PositiveIntegerField(default=0)
    kustomization = models.PositiveSmallIntegerField()
    owner = models.ForeignKey(Account)
    orbiting = models.ForeignKey(Planet)
    garrison = models.ForeignKey(Garrison)
    garrison_orders = ArmyOrder()

    def __unicode__(self):
        return unicode(self.name)

    def canRelocate(self):
        '''Returns False if either:
            - has no engine
            - is relocating
            - is evacuating/dropping
           Else returns True'''
        from bellum.orders.models import MotherRelocationOrder, LandarmyMotherPickupOrder, LandarmyPlanetaryStrikeOrder
        if self.b_0 == 0: return False
        if self.isRelocating(): return False
        if self.landarmyplanetarystrikeorder_set.count() > 0: return False
        if self.landarmymotherpickuporder_set.count() > 0: return False
        return True

    def duePosition(self):
        '''If not relocating, return orbiting. Else return relocation target'''
        if not self.isRelocating(): return self.orbiting
        return self.motherrelocationorder_set.all()[0].loc_to

    def isRelocating(self):
        from bellum.orders.models import MotherRelocationOrder
        try:
            self.motherrelocationorder_set.all()[0]
        except:
            return False
        return True
        raise Exception, 'Invalid codepath'

    def getRelocation(self):
        if not self.isRelocating(): raise Exception, 'Not relocating'   # It's not a check really, it populates cache__relocation
        return self.motherrelocationorder_set.all()[0]

    def getConstructionLevelById(self, id):
        return self.__dict__['b_' + str(id)] 

    def getConstructions(self):
        from bellum.orders.models import MotherConstructionOrder
        mobs = MotherConstructionOrder.objects.filter(mother=self)
        return map(lambda x: x.what, mobs)

    def getLandarmyProductions(self):
        from bellum.orders.models import LandarmyProduceOrder
        lpos = LandarmyProduceOrder.objects.filter(mother=self)
        return lpos

    def getConstructionObjects(self):
        from bellum.orders.models import MotherConstructionOrder
        return MotherConstructionOrder.objects.filter(mother=self)

    def getConstructionObject(self, what):
        from bellum.orders.models import MotherConstructionOrder
        return MotherConstructionOrder.objects.filter(mother=self).get(what=what)

    def setConstructionLevelById(self, id, lvl):
        self.__dict__['b_' + str(id)] = lvl

    def getPendingConstructionsCount(self):
        from bellum.orders.models import MotherConstructionOrder
        return len(MotherConstructionOrder.objects.filter(mother=self))

    def getResearches(self):
        from bellum.orders.models import TechnologyResearchOrder
        mobs = TechnologyResearchOrder.objects.filter(mother=self)
        return map(lambda x: x.what, mobs)

    def getResearchObjects(self):
        from bellum.orders.models import TechnologyResearchOrder
        return TechnologyResearchOrder.objects.filter(mother=self)

    def getResearchObject(self, what):
        from bellum.orders.models import TechnologyResearchOrder
        return TechnologyResearchOrder.objects.filter(mother=self).get(what=what)

    def getPendingResearchesCount(self):
        from bellum.orders.models import TechnologyResearchOrder
        return len(TechnologyResearchOrder.objects.filter(mother=self))
        

class Technology(models.Model):
    owner = models.OneToOneField(Account)
    o_0 = models.PositiveSmallIntegerField(default=0)    # defensive systems
    o_1 = models.PositiveSmallIntegerField(default=0)    # nanobot armor
    o_2 = models.PositiveSmallIntegerField(default=0)    # excavation
    o_3 = models.PositiveSmallIntegerField(default=0)    # diamond drills
    o_4 = models.PositiveSmallIntegerField(default=0)    # engineering
    o_5 = models.PositiveSmallIntegerField(default=0)    # Lab Const Plans
    o_6 = models.PositiveSmallIntegerField(default=0)    # Hangar Const Plans
    o_7 = models.PositiveSmallIntegerField(default=0)    # Ex Hangar Const Plans
    o_8 = models.PositiveSmallIntegerField(default=0)    # offensive systems
    o_9 = models.PositiveSmallIntegerField(default=0)    # small cal artillery
    o_10 = models.PositiveSmallIntegerField(default=0)   # big cal artillery
    o_11 = models.PositiveSmallIntegerField(default=0)   # sniper
    o_12 = models.PositiveSmallIntegerField(default=0)   # logistics
    o_13 = models.PositiveSmallIntegerField(default=0)   # science
    o_14 = models.PositiveSmallIntegerField(default=0)   # supercomputer
    o_15 = models.PositiveSmallIntegerField(default=0)   # racial tech
    o_16 = models.PositiveSmallIntegerField(default=0)   # counterespionage

    def setTechnologyLevelById(self, id, lvl):
        self.__dict__['o_' + str(id)] = lvl
    
    def getTechnologyLevelById(self, id):
        return self.__dict__['o_' + str(id)]

class TradeOffer(models.Model):
    mother = models.ForeignKey(Mother)        # one offering resources
    titan_p = models.IntegerField()
    pluton_p = models.IntegerField()        # offerer wants to give P resources for F
    men_p = models.IntegerField()
    titan_f = models.IntegerField()
    pluton_f = models.IntegerField()
    men_f = models.IntegerField()