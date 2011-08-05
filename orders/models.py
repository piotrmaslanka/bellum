# coding=UTF-8
from django.db import models
from datetime import datetime
from bellum.common.models import XYPosition
from bellum.register.models import Account
from bellum.mother.models import Mother, Technology
from bellum.space.models import Planet
from bellum.province.models import ProvintionalPresence
from bellum.landarmy.models import ArmyOrder as LandarmyOrder, Garrison as LandarmyGarrison
from bellum.province.models import Province
from bellum.common.utils import datetime__secondsToNow, STRIKEORDER_DESIGNATION

GOT_ORDERTYPE = ((0, 'MotherRelocationOrder'),
                 (1, 'MotherConstructionOrder'),
                 (2, 'TechnologyResearchOrder'),
                 (3, 'ProvinceBuildOrder'),
                 (4, 'ResourceSendOrder'),
                 (5, 'LandarmyProduceOrder'),
                 (6, 'LandarmyPlanetaryStrikeOrder'),
                 (7, 'LandarmyProvintionalStrikeOrder'),
                 (8, 'LandarmyMotherPickupOrder'),
                 )
 
class GenericOrderTable(models.Model):
    to_be_completed = models.DateTimeField(db_index=True)
    ordered_on = models.DateTimeField()
    ordertype = models.PositiveSmallIntegerField(choices=GOT_ORDERTYPE)
    def secondsToCompletion(self):
        return datetime__secondsToNow(self.to_be_completed)
    def secondsSinceStart(self):
        return datetime.now() - self.ordered_on
    def duration(self):
        return self.to_be_completed - self.ordered_on

    def reverseTransformata(self):
        if self.to_be_completed < datetime.now():
            t = self.duration()
            self.ordered_on = self.to_be_completed
            self.to_be_completed = self.ordered_on + t
        else:
            t = datetime.now() - self.ordered_on
            self.ordered_on = datetime.now()
            self.to_be_completed = self.ordered_on + t



class BaseOrder(models.Model):
    got = models.ForeignKey(GenericOrderTable)
    class Meta:
        abstract = True

class ProvinceBuildOrder(BaseOrder):
    ppresence = models.ForeignKey(ProvintionalPresence)
    what = models.PositiveSmallIntegerField()
    slot = models.PositiveSmallIntegerField()
   
class TechnologyResearchOrder(BaseOrder):
     what = models.PositiveSmallIntegerField()
     mother = models.ForeignKey(Mother)   
   
class MotherRelocationOrder(BaseOrder):
    loc_from = models.ForeignKey(Planet, related_name='relocating_mothers_from', db_index=False)
    loc_to = models.ForeignKey(Planet, related_name='relocating_mothers_to', db_index=False)
    mother = models.ForeignKey(Mother)
    
class MotherConstructionOrder(BaseOrder):
    what = models.PositiveSmallIntegerField()
    mother = models.ForeignKey(Mother)
    
class ResourceSendOrder(BaseOrder):
    titan = models.PositiveIntegerField()
    pluton = models.PositiveIntegerField()
    men = models.PositiveIntegerField()
    send_to = models.ForeignKey(Mother, related_name='receiver')
    send_from = models.ForeignKey(Mother, related_name='sender')

class LandarmyProduceOrder(BaseOrder):
    mother = models.ForeignKey(Mother)
    sold_nr = models.PositiveSmallIntegerField()     # from zero to n
    amount = models.PositiveIntegerField()
    maketime = models.PositiveIntegerField()        # time of single soldier production

class LandarmyMotherPickupOrder(BaseOrder):
    mother = models.ForeignKey(Mother)
    province = models.ForeignKey(Province)
    garrison = models.ForeignKey(LandarmyGarrison)

class LandarmyPlanetaryStrikeOrder(BaseOrder):
    mother = models.ForeignKey(Mother)
    province = models.ForeignKey(Province)
    garrison = models.ForeignKey(LandarmyGarrison)
    designation = models.PositiveSmallIntegerField(choices=STRIKEORDER_DESIGNATION)
    orders = LandarmyOrder()

    def fallback(self):
        got = self.got
        garrison = self.garrison
        province = self.province
        mother = self.mother

        lmpo = LandarmyMotherPickupOrder(None, got.id, mother.id, province.id, garrison.id)

        got.reverseTransformata()
        got.ordertype = 8
        got.save()
        lmpo.save()
        self.delete()

        if got.to_be_completed < datetime.now():
            from bellum.orders.mother.landarmy_mpickup import doLandarmyMotherPickupOrder
            from bellum.orders import DontRemoveGOT
            try:
                doLandarmyMotherPickupOrder(lmpo)
            except DontRemoveGOT:
                pass
            else:
                got.delete()

    
class LandarmyProvintionalStrikeOrder(BaseOrder):
    attacker = models.ForeignKey(Account)
    srcprovince = models.ForeignKey(Province, related_name='landarmyprovintionalstrike_src')
    dstprovince = models.ForeignKey(Province, related_name='landarmyprovintionalstrike_dst')
    garrison = models.ForeignKey(LandarmyGarrison)
    designation = models.PositiveSmallIntegerField(choices=STRIKEORDER_DESIGNATION)
    orders = LandarmyOrder()

    def directiveFallback(self, designation=0):
        '''Just fallback. Does save both GOT and order.'''
        srcp = self.srcprovince
        self.srcprovince = self.dstprovince
        self.dstprovince = srcp

        self.designation = designation

        self.got.reverseTransformata()
        self.got.save()
        self.save()

        if self.got.to_be_completed < datetime.now():       # ie. this was just completed
            from bellum.orders.province.landarmy_pstrike import doLandarmyProvintionalStrike
            from bellum.orders import DontRemoveGOT
            try:
                doLandarmyProvintionalStrike(self.got, self)
            except DontRemoveGOT:
                pass
            else:
                self.got.delete()

