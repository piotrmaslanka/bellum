from bellum.common.models import ResourceIndex
from bellum.space.models import Planet
from bellum.mother.models import Mother, Technology
from bellum.landarmy.models import Garrison
import datetime
from bellum.stats import STATDATABASE_ROOT
from bellum.common.smf.processes import registerAccount

MAX_PLAYERS_PER_PLANET = 2
INTERPLAYER_DELAY = datetime.timedelta(7)       # a week

def getPlanetId():
    # TODO: Acquire global lock on allocator!!
    pllist = eval(open(STATDATABASE_ROOT+'planetlist.nsal', 'r').read())
    cpid, pdate, psofar = eval(open(STATDATABASE_ROOT+'allocatorstatus.nsal', 'r').read())

    get_new_planet = False
    if pdate != None:
        if (datetime.datetime.now() - pdate) > INTERPLAYER_DELAY:
            get_new_planet = True

    if psofar >= MAX_PLAYERS_PER_PLANET:
        get_new_planet = True

    if get_new_planet:
        cpid = pllist[0]
        open(STATDATABASE_ROOT+'planetlist.nsal', 'w').write(repr(pllist[1:]))
        psofar = 0

    # OK, current planet id is CPID
    psofar += 1
    pdate = datetime.datetime.now()

    open(STATDATABASE_ROOT+'allocatorstatus.nsal', 'w').write(repr((cpid, pdate, psofar)))

    # TODO: Free global lock on allocator!!

    return cpid


from bellum.common.fixtures.resources.recalculate import recalc

def activate(account):
    r = ResourceIndex(lastupdated=datetime.datetime.now(), titan=3000, pluton=3000, men=800)
    r.save()
    account.resources = r
    account.save()

    Technology(owner=account).save()
    g = Garrison()
    g.save()

    pid = getPlanetId()

    Mother(name=u'Statek-matka', kustomization=0, owner=account, orbiting=Planet.objects.get(id=pid), garrison=g, garrison_orders=0).save()

    recalc(account)

    registerAccount(account.login, account.password, account.email, account.empire)
