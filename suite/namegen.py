# coding=UTF-8
'''Suite is a collection of tools to perform deployment tasks.
Right now, called suite will generate 100 random planets with 6 provinces each'''
from random import random, shuffle

class Resources:
    VOWELS = ['a', 'e', 'i', 'o', 'u']
    CONSONANTS = ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'r', 's', 't', 'w', 'z']

class GenericNameGenerators:
    @staticmethod
    def genORKY2(START, VOWELS, CONS, END):
        start = START
        vowels = VOWELS
        cons = CONS
        end = END
        shuffle(start)
        name = start[0]
        if name[-1] in cons + ['y']:
            vowel = True
        else:
            vowel = False


        for i in range(0, int(random()*3)):
            if vowel:
                shuffle(vowels)
                name = name + vowels[0]
                vowel = False
            else:
                shuffle(cons)
                name = name + cons[0]
                vowel = True
        shuffle(end)

        if end[0][-1] in cons:
            shuffle(vowels)
            name = name + vowels[0]
        if end[0][-1] in vowels:
            shuffle(cons)
            name = name + cons[0]

        return name + end[0]

    @staticmethod
    def comboFilter(s, combos):
        for c in combos:
            s = s.replace(c, c[0])
            s = s.replace(c[1] + c[0], c[1])
        return s

    @staticmethod
    def adjacentFilter(s):
        '''Makes no two same letters appear together'''
        for l in Resources.VOWELS + Resources.CONSONANTS:
            s = s.replace(l + l, l)
        return s

    @staticmethod
    def coO2():
        START = ['iso','mer', 'cy', 'sy', 'tar', 'sar', 'mar', 'far', 'nar', 'ura', 'pla', 'nus', 've', 'an', 'ez']
        VOWELS = Resources.VOWELS
        CONS = Resources.CONSONANTS
        COMBOS = ['cv', 'rz', 'kv', 'tf', 'mv' , 'pm', 'fv', 'rv', 'bv', 'zv', 'xv', 'pv' , 'yt', 'wv', 'yh', 'dc']
        END = ['tar', 'mar', 'rus', 'cus', 'ne', 'ry', 'va', 'yth', 'no', 'so', 'ko']
        xnam= GenericNameGenerators.comboFilter(GenericNameGenerators.adjacentFilter(GenericNameGenerators.genORKY2(START, VOWELS, CONS, END)), COMBOS)
        xnam = xnam[0].capitalize() + xnam[1:]
        return xnam

def getName():
    return GenericNameGenerators.coO2()