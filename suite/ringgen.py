# coding=UTF-8
from __future__ import division
from suite.mathops import polar_to_cartesian, getStandarizedGauss

class RingDefinition(object):
    def __init__(self, r, width, anglestep):
        '''r and width should be as if the map was a (-1, -1) to (1, 1) square. Anglestep is expressed in degrees'''
        self.r = r
        self.width = width
        self.anglestep = anglestep
        self.stepcounter = 0
    def advance(self):
        self.stepcounter += self.anglestep
    def getrandomcoords(self):
        '''returns in polar coordinates!'''
        r = self.r + getStandarizedGauss() * self.width
        return (r, self.stepcounter)
        
def fillin(tab, priindex, secindex):
    try:
        tab[priindex]
    except:
        tab[priindex] = {}
    try:
        tab[priindex][secindex]
    except:
        tab[priindex][secindex] = True

def sumup(tab, stab):
    for kx, v in stab.iteritems():
        for ky, l in v.iteritems():
            fillin(tab, kx, ky)


def generate(psX, psY, ring):
    '''psX, psY - prescalers for x, y'''
    map = {}
    while ring.stepcounter < 360:
        x, y = polar_to_cartesian(*ring.getrandomcoords())
        x *= psX
        y *= psY
        fillin(map, int(x), int(y))
        ring.advance()
    return map
