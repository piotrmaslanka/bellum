# coding=UTF-8
from bellum.meta import MGI
from django.db import models
from django import forms
import re

class ArmyOrder(models.IntegerField):
    def get_internal_type(self):
        return "ArmyOrder"
    def db_type(self):
        return 'bigint'    

class Garrison(models.Model):
    st0 = models.PositiveIntegerField(default=0)
    st1 = models.PositiveIntegerField(default=0)
    st2 = models.PositiveIntegerField(default=0)
    st3 = models.PositiveIntegerField(default=0)    
    st4 = models.PositiveIntegerField(default=0)
    st5 = models.PositiveIntegerField(default=0)
    st6 = models.PositiveIntegerField(default=0)
    st7 = models.PositiveIntegerField(default=0)
    st8 = models.PositiveIntegerField(default=0)    
    st9 = models.PositiveIntegerField(default=0)
    st10 = models.PositiveIntegerField(default=0)
    st11 = models.PositiveIntegerField(default=0)
    st12 = models.PositiveIntegerField(default=0)
    st13 = models.PositiveIntegerField(default=0)
    st14 = models.PositiveIntegerField(default=0)
    st15 = models.PositiveIntegerField(default=0)
    st16 = models.PositiveIntegerField(default=0)
    st17 = models.PositiveIntegerField(default=0)
    st18 = models.PositiveIntegerField(default=0)
    st19 = models.PositiveIntegerField(default=0)


    def isZero(self):
        '''Checks whether garrison is empty'''
        for y in xrange(0, 20):
            if self[y] > 0:
                return False
        return True

    def __unicode__(self):
        x = u'Garrison ('
        for y in xrange(0, 20):
            x += unicode(str(self[y])+u', ')
        return x + u')'

    def __eq__(self, tgt):
        if tgt in (0, None):
            for x in xrange(0, 20):
                if self[x] > 0:
                    return False
            return True
        return None
    
    def __iadd__(self, garrison):
        for x in xrange(0, 20):
            self[x] += garrison[x]
        return self 

    def __isub__(self, garrison):
        for x in xrange(0, 20):
            self[x] -= garrison[x]
            if self[x] < 0:     # Anti-Minus Protection
                self[x] = 0
        return self

    def __sub__(a, b):
        x = Garrison()
        for i in xrange(0, 20):
            x[i] = a[i] - b[i]
            if x[i] < 0: x[i] = 0   # Anti-Minus Protection
        return x

    def __add__(a, b):
        x = Garrison()
        for i in xrange(0, 20):
            x[i] = a[i] + b[i]
        return x
    
    def __contains__(self, gar):
        for x in xrange(0, 20):
            if self[x] < gar[x]:
                return False
        return True

    def assign(self, gar):  # DEPRECATED; use clone() instead
        self.clone(gar)

    def clone(self, gar):
        '''Should be more properly called assign, because it extracts info to self from another garrison'''
        for x in xrange(0, 20):
            self[x] = gar[x]

    def __getitem__(self, key):
        return self.__dict__['st'+str(key)]

    def __setitem__(self, key, value):
        self.__dict__['st'+str(key)] = value
    
_interpolateGarrisonre = re.compile('st[0-9]{1,2}')    
    
def interpolateGarrison(obj):
    '''Creates a Garrison from an arbitrary object having st0..st19 parameters'''
    mdict = {}
    for iname, ival in obj.__dict__:
        if _interpolateGarrisonre.match(iname):
            mdict[iname] = ival
    return Garrison(**mdict)

def cloneGarrison(gar):
    ngar = Garrison()
    ngar.assign(gar)
    return ngar