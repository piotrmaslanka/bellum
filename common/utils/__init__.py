# coding=UTF-8
from __future__ import division
import locale
from datetime import datetime
from bellum.meta import MGID
from bellum.common.fixtures.landarmy_stats import UNIT_NAMES

class SystemWideLock(object):
    def __init__(self, lockname=None):
        pass
    def acquire(self):
        return self
    def release(self):
        return self


def datetime__secondsToNow(time):
    dt = time - datetime.now()
    return dt.days * 86400 + dt.seconds

def timedelta__seconds(time):
    return time.days * 86400 + time.seconds

STRIKEORDER_DESIGNATION = ((0, u'Wycofywuję się'),
                           (1, u'Atak jeśli nie sprzymierzona gdy przyleci, inaczej Wspomóż'),
                           (2, u'Atak'),
                           (3, u'Wycofaj jeśli nie sprzymierzona gdy przyleci, inaczej Wspomóż'),
                           (4, u'Wspomóż'),
                           (5, u'[DEBUG]Wycofaj się przy przylocie'),
                          )

def coma(x):
    x = int(x)
    locale.setlocale(locale.LC_ALL, 'en_US')
    return locale.format("%d", x, grouping=True)

def humanize__designation(des):
    for id, txt in STRIKEORDER_DESIGNATION:
        if des == id:
            return txt

def humanize__convertSeconds(secs):
    days = int(secs // 86400)
    secs = secs - days * 86400
    hours =  int(secs // 3600)
    secs = secs - hours * 3600
    minutes = int(secs // 60)
    secs = secs - minutes * 60
    seconds = int(secs)

    if days > 0:
        return unicode(days)+u' d '+unicode(hours)+u':'+unicode(minutes)+u':'+unicode(seconds)
    elif hours > 0:
        return unicode(hours)+u':'+unicode(minutes)+u':'+unicode(seconds)
    elif minutes > 0:
        return unicode(minutes)+u':'+unicode(seconds)
    else:
        return unicode(seconds)+u' s'

def htmlize__garrison(garr, race):
    '''used for Planetary, with garrison tooltops'''
    tt = u'<span style=\\\'font-weight: bold; font-size: 1.5em;\\\'>'

    for x in xrange(0, MGID+1):
        if garr[x] > 0:
            tt += UNIT_NAMES[race][x]+u': '+str(garr[x])+u'<br>'
    tt += '</span>'
    return tt

def htmlize__costs(rindexp):
    '''rindexp is a tuple (ResourceIndex, TimeInSeconds)'''
    tt = u'<span style=\\\'font-weight: bold; font-size: 1.5em;\\\'>'

    tt += u'Tytan: '+unicode(rindexp[0].titan)+u'<br>'
    tt += u'Pluton: '+unicode(rindexp[0].pluton)+u'<br>'
    tt += u'Manpower: '+unicode(rindexp[0].men)+u'<br>'
    tt += u'Czas: '+humanize__convertSeconds(rindexp[1])+u'<br>'
    tt += u'</span>'
    return tt

def htmlize__requirement(vs):
    tt = u'<span style=\\\'font-weight: bold; font-size: 1.5em;\\\'>'

    for name, passed, lvl in vs:
        tt = tt + u'<span style=\\\'color: '
        if passed:
            tt = tt + u'rgb(63, 205, 0);'
        else:
            tt = tt + u'rgb(237, 142, 56);'
        tt = tt + '\\\'>' + unicode(name) + u': ' + unicode(lvl) + u'</span><br>'
    tt = tt + u'</span>'
    return tt

def humanize__timeago(dt):
    s = timedelta__seconds(datetime.now() - dt)
    if s < 119: return u'Minutę temu'
    if s < 299: return u'' + str(s//60) + ' minuty temu'
    if s < 3600: return u'' + str(s//60) + ' minut temu'
    if s < 7199: return u'Godzinę temu'
    if s < 17999: return u'' + str(s//3600) + ' godziny temu'
    if s < 86400: return u'' + str(s//3600) + ' godzin temu'
    if s < 172799: return u'Dzień temu'
    return u'' + str(s // 86400) + ' dni temu'

def humanize__requirement(requirement, metmum=None, mettech=None):
    dontcheck = (mettech==None) and (metmum==None)
    vs = []
    from bellum.common.fixtures.technology import TECHNOLOGY_NAMES
    from bellum.common.fixtures.mother_construction import CONSTRUCTION_NAMES

    for cn in requirement.req_array:
        i = int(cn[2:])
        lv = requirement.__dict__[cn]
        if cn[0] == 'c':
           v1 = CONSTRUCTION_NAMES[i]
           if not dontcheck:
               v2 = requirement.checkConstructionByMotherSingle(metmum, i, lv)
           else:
               v2 = None
        if cn[0] == 't':
           v1 = TECHNOLOGY_NAMES[i]
           if not dontcheck:
               v2 = requirement.checkTechnologySingle(mettech, i, lv)
           else:
               v2 = None
        vs.append((v1, v2, lv))
    return vs    