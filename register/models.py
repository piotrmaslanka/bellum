# coding=UTF-8
from django.db import models
from django import forms
from datetime import datetime
from bellum.common.models import CSCharField
from bellum.common.models import ResourceIndex

ACCOUNT_RACE = ((0, 'Partia'),
                (1, 'Magnuss'),
                (2, 'Technokraci'),
               )
ACCOUNT_PRIV = ((0, 'Gracz'),
                (1, 'Administrator')
               )
ACCOUNT_SEX = ((0, 'Nieokreślone'),
               (1, 'Mężczyzna'),
               (2, 'Kobieta'),
              )
BIRTHDAY_DAY = ((0, '1'), (1, '2'), (2, '3'), (3, '4'), (4, '5'), (5, '6'), (6, '7'), (7, '8'),(8, '9'), (9, '10'), (10, '11'), (11, '12'), (12, '13'), (13, '14'), (14, '15'), (15, '16'), (16, '17'), (17, '18'), (18, '19'), (19, '20'), (20, '21'), (21, '22'), (22, '23'), (23, '24'), (24, '25'), (25, '26'), (26, '27'), (27, '28'), (28, '29'), (29, '30'), (30, '31')) 
BIRTHDAY_MONTH = ((0, u'Styczeń'), (1, u'Luty'), (2, u'Marzec'), (3, u'Kwiecień'), (4, u'Maj'), (5, u'Czerwiec'), (6, u'Lipiec'), (7, u'Sierpień'),(8, u'Wrzesień'), (9, u'Październik'), (10, u'Listopad'), (11, u'Grudzień')) 

class Account(models.Model):
    '''Player account model'''
    login = models.CharField(max_length=20, unique=True, db_index=True)
    password = CSCharField(max_length=40, db_index=True)
    email = models.EmailField(max_length=50, unique=True)
    race = models.PositiveSmallIntegerField(choices=ACCOUNT_RACE, default=0)
    priv = models.PositiveSmallIntegerField(choices=ACCOUNT_PRIV, default=0)
    registered_on = models.DateTimeField(default=datetime.now)
    banexpire = models.DateTimeField(null=True, default=None)
    banreason = models.TextField(default=None, null=True)
    birthdate_year = models.PositiveSmallIntegerField(null=True, blank=True)
    birthdate_month = models.PositiveSmallIntegerField(choices=BIRTHDAY_MONTH, null=True, blank=True)
    birthdate_day = models.PositiveSmallIntegerField(choices=BIRTHDAY_DAY, null=True, blank=True)
    sex = models.PositiveSmallIntegerField(choices=ACCOUNT_SEX, default=0)
    signature = models.TextField(null=True, blank=True, default=None)
    points = models.IntegerField(default=0)
    empire = models.CharField(max_length=40, unique=True)
    resources = models.OneToOneField(ResourceIndex, null=True)
    is_avatar = models.PositiveSmallIntegerField(default=0)     # 0 - no avatar, 1 - avatar set

    def getPendingResearchesCount(self):
        from bellum.orders.models import TechnologyResearchOrder
        return len(TechnologyResearchOrder.objects.filter(mother__owner=self))
    
class RegisterConfirmation(models.Model):
    '''A register confirmation. Used to store information needed to confirm new accounts'''
    from datetime import datetime
    account = models.ForeignKey(Account)
    key = CSCharField(max_length=40, db_index=True, unique=True)
    registered_on = models.DateTimeField(db_index=True, default=datetime.now)


def generate_random_password():
    from random import choice
    stuff = range(97, 123) + range(48, 58)
    passw = ''
    for i in xrange(0, 8):
        passw += chr(choice(stuff))
    return passw

class PasswordRemindToken(models.Model):
    from datetime import datetime
    account = models.ForeignKey(Account)
    newpassword = models.CharField(max_length=8, default=generate_random_password)
    key = CSCharField(max_length=40, db_index=True, unique=True)
    generated_on = models.DateTimeField(db_index=True, default=datetime.now)

        
