from __future__ import division
from bellum.province.models import ProvintionalPresence
from bellum.mother.models import Mother
from bellum.common.models import ResourceIndex   
from math import pow


def calculate_presence(ppresence):
    '''this operates in resource per hour'''
    x = ResourceIndex()

    for i in xrange(0, ppresence.province.slots):
        otype, olvl = ppresence.getPair(i)
        if otype == 1:
            x.ratio_titan += (pow(1.5, olvl-1) * 48) * ppresence.province.titan_coef
        if otype == 2:
            x.ratio_pluton += (pow(1.5, olvl-1) * 36) * ppresence.province.pluton_coef
        if otype == 3:
            x.ratio_men += (pow(1.5, olvl-1) *23) * ppresence.province.town_coef
    return x


def calculate_mother(mum):
    '''this operates in resource per hour'''
    x = ResourceIndex(ratio_titan=0, ratio_pluton=0, ratio_men=0)
    if mum.b_2 > 0:
        x.ratio_titan += pow(1.5, mum.b_2-1) * 30
        x.ratio_pluton += pow(1.5, mum.b_2-1) * 15
    if mum.b_1 > 0:
        x.ratio_men += pow(1.5, mum.b_1-1) * 8

    x.ratio_men += 10
    x.ratio_titan += 30
    x.ratio_pluton += 20
    return x

def apply_technology(technology, rindex):
    gtp = technology.o_2*0.05 + (technology.o_3 * 0.2) # 5% from excavation, 20% from drills

    rindex.ratio_titan *= 1 + gtp
    rindex.ratio_pluton *= 1 + gtp

    return rindex

def recalc(PlayerAccount):
    '''Recalculates player resource income'''
    ppresences = ProvintionalPresence.objects.filter(owner=PlayerAccount)
    ratio = ResourceIndex(ratio_titan=0, ratio_pluton=0, ratio_men=0)

    for ppresence in ppresences:
        ratio.addRatio(calculate_presence(ppresence))
        

    for mum in Mother.objects.filter(owner=PlayerAccount):
        ratio.addRatio(calculate_mother(mum))

        
    ratio.ratio_titan = ratio.ratio_titan / 3600
    ratio.ratio_pluton = ratio.ratio_pluton / 3600
    ratio.ratio_men = ratio.ratio_men / 3600                # convert all to resource per second
        
    ratio = apply_technology(PlayerAccount.technology, ratio)
        
    rindex = PlayerAccount.resources
    rindex.stateUpdate()
    rindex.setRatio(ratio.ratio_titan, ratio.ratio_pluton, ratio.ratio_men)
    rindex.save()
