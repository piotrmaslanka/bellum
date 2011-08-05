from __future__ import division
from math import pow
from random import random

def throw(chance):
    '''returns True if we have passed a chance for given check, False otherwise'''
    return random() <= chance

def provintionalpresence_to_im(presence):
    '''calculates Im from sum of building levels'''
    total = presence.s0lvl
    total += presence.s1lvl
    total += presence.s2lvl
    total += presence.s3lvl
    total += presence.s4lvl
    return (1-pow(0.9, total)) / 2

def province_to_dbm(province):
    '''calculates Pm from a province'''
    return pow(0.9, 1-province.natural_defense_level)