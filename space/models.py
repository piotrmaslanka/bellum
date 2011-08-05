# coding=UTF-8
from __future__ import division
from django.db import models
from bellum.common.models import XYPosition, BigIntegerField
from bellum.register.models import Account

PLANET_KIND = ((0, 'Startowa'),
               (1, 'Zwykła'),
               (2, 'Niebiańskie'),
               (3, 'Exterminatus'),
              )

class PlanetProvintionalLinkCapacity(models.Model):
    strdat = models.CharField(max_length=20) # sufficient for 17 provinces
        # to get bit number one accesses char at bit div 8, then a bit described by bit mod 8.
        # strange to write, easy to understand

#       Watch out! Maths come in play here.
#       Storing a symmetric matrix of row size n where M[x][x] == moot requires at most (n(n-1)/2) bits
#       Therefore storing 10 rows will consume 55 bits, but 11 will 66.
#       We can deploy only 64, and then we will have to worry about 2-complementary and sign bits, so we can use 63 bits.
#       This sucks. Therefore if 62th bit(0th bit is first) in path_graph is set, bits 61...0 are ID to
#       PlanetProvintionalLinkCapacity which can represent up to OMFG-LOTS-OF connections, but is slower
#       Therefore, we need a nitty-gritty constant to simplify our calculations. There it comes:
PATH_GRAPH_DETERMINATA = 4611686018427387903L   # (1 << 62)-1

class Planet(XYPosition):
    name = models.CharField(max_length=20)
    kind = models.PositiveSmallIntegerField(choices=PLANET_KIND)
    path_graph = BigIntegerField()
    kustomization = models.PositiveSmallIntegerField()
    amount_of_provinces = models.PositiveSmallIntegerField()   # ^ - redundant, computable from COUNT() WHERE planet=this, but made for speed

    def isLink(self, a, b):
        '''Provinces are a,b. They are numbered from 0 to n'''
        if a==b:
            return True
        if b > a:       # make it so a>b
            x = a
            a = b
            b = x
        chkbit = ((a-1)*a)//2 + b        # from zero to n
        if self.path_graph > PATH_GRAPH_DETERMINATA:    # it is not trivial...
            pplc = PlanetProvintionalLinkCapacity.objects.get(id=self.path_graph & PATH_GRAPH_DETERMINATA)
            return (ord(pplc.strdat[chkbit // 8]) & (1 << (chkbit % 8))) > 0
        else:
            return ((self.path_graph & (1 << chkbit)) > 0)


class LinkingSetter(object):
    def __init__(self, planet, max_provinces):
        self.isPPLC = False
        self.tso = planet       # To-Save-Object. Cache friend ^_^
        if max_provinces > 10:
            self.isPPLC = True
            b = u'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
            pplc = PlanetProvintionalLinkCapacity(None, b)
            pplc.save()
            planet.path_graph = PATH_GRAPH_DETERMINATA + 1 + pplc.id
            planet.save()
            self.tso = pplc

    def __del__(self):
        self.tso.save()

    def set(self, a, b):
        '''Slow!'''
        if b > a:
            x = a
            a = b
            b = x
        chkbit = ((a-1)*a)//2 + b        # from zero to n
        if self.isPPLC:
            pplc = self.tso
            lv = list(pplc.strdat)
            pa, pb = chkbit // 8, chkbit % 8
            lv[pa] = chr(ord(lv[pa]) | (1<<pb))
            pplc.strdat = ''.join(lv)
        else:
            self.tso.path_graph = self.tso.path_graph | (1<<chkbit)

