# coding=UTF-8
from django.db import models
from bellum.register.models import Account

LAM_CHOICES = ((1, "Strona sojuszu"),
               (2, "Uprawnienia"),
               (4, "Wykopywanie"),
               (8, "Przyjmowanie"),
               (16, "Moderacja"))
AM_TEAMSITE = 1
AM_PRIVILEGE = 2
AM_KICK = 4
AM_ACCEPT = 8
AM_MODERATE = 16

class Alliance(models.Model):
    name = models.CharField(max_length=30, blank=False, null=False, unique=True)
    shname = models.CharField(max_length=5, blank=False, null=False, unique=True)
    members = models.PositiveIntegerField(default=0)
    points = models.PositiveIntegerField(default=0) # unused
    leader = models.ForeignKey(Account)
    mainpage = models.TextField(blank=False, null=False, default=None)
    is_avatar = models.PositiveSmallIntegerField(default=0)     # 0 - no avatar, 1 - avatar set as PNG, 2 - avatar set as GIF
    smf_board_id = models.PositiveIntegerField()
    smf_group_id = models.PositiveIntegerField()     # smf bookkeeping data

class AllianceMembership(models.Model):
    account = models.ForeignKey(Account)
    alliance = models.ForeignKey(Alliance)
    privileges = models.PositiveIntegerField(default=0)
    rank = models.CharField(max_length=20)

    def toChoicesList(self):
        def lstA(list, privilege, obj):
            if obj.hasPrivilege(privilege):
                list.append(privilege)
        list = []
        lstA(list, AM_TEAMSITE, self)
        lstA(list, AM_PRIVILEGE, self)
        lstA(list, AM_KICK, self)
        lstA(list, AM_ACCEPT, self)
        lstA(list, AM_MODERATE, self)
        return list

    def fromChoicesToPrivileges(self, chlist):
        self.privileges = 0
        for x in chlist:
            self.privileges = self.privileges | int(x)
        
    def hasPrivilege(self, privilege):
        return (self.privileges & privilege) > 0

class AllianceApplication(models.Model):
    applicant = models.ForeignKey(Account)
    alliance = models.ForeignKey(Alliance)
    message = models.TextField()

