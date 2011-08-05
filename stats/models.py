# coding=UTF-8
from django.db import models
from os import rename
from bellum.stats import REPORT_ROOT, REPORT_ROOT__RECLAMATION_POOL
import cPickle as pickle
from bellum.register.models import Account
from bellum.alliance.models import Alliance

class Report(models.Model):
    reflinks = models.PositiveIntegerField(default=0)
    title = models.CharField(max_length=50)

    def __repr__(self):
        return 'Report object: '+str(self.id)

    @staticmethod
    def create(repdata, title):
        rep = Report(title=title)
        rep.save()
        pickle.dump(repdata, open(REPORT_ROOT+str(rep.id),'wb'))
        rep.data = repdata
        return rep

    def unlink(self):
        self.reflinks -= 1
        if self.reflinks == 0:
            rename(REPORT_ROOT+str(self.id), REPORT_ROOT__RECLAMATION_POOL+str(self.id))
            self.delete()
        else:
            self.save()
            
    def link(self):
        self.reflinks += 1
        self.save()
        
    def __getattr__(self, name):
        if name == 'data':
            self.data = pickle.load(open(REPORT_ROOT+str(self.id), 'rb'))
            return self.data

class RankingNone(models.Model):        # all spending ranking
    shname = models.CharField(max_length=5)
    alliance_id = models.PositiveIntegerField()
    empire = models.CharField(max_length=40)
    account = models.ForeignKey(Account)
    points = models.PositiveIntegerField()
    delta = models.IntegerField()

class RankingMother(models.Model):        # mothership ranking
    shname = models.CharField(max_length=5)
    alliance_id = models.PositiveIntegerField()
    empire = models.CharField(max_length=40)
    account = models.ForeignKey(Account)
    points = models.PositiveIntegerField()
    delta = models.IntegerField()

class RankingArmy(models.Model):        # army spending ranking
    shname = models.CharField(max_length=5)
    alliance_id = models.PositiveIntegerField()
    empire = models.CharField(max_length=40)
    account = models.ForeignKey(Account)
    points = models.PositiveIntegerField()
    delta = models.IntegerField()

class RankingAlliance(models.Model):
    shname = models.CharField(max_length=5)
    name = models.CharField(max_length=30, blank=False, null=False, unique=True)
    members = models.PositiveIntegerField(default=0)
    alliance = models.ForeignKey(Alliance)
    points = models.PositiveIntegerField()
    delta = models.IntegerField()
