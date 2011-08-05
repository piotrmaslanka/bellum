from bellum.province.models import Province, ProvintionalPresence
from bellum.orders.models import ProvinceBuildOrder, GenericOrderTable
from bellum.common.fixtures.resources import recalc
from datetime import datetime
from time import time
from bellum.stats.igstatistics.resources_sent import note

def doProvinceBuildOrder(entry):
    pp = ProvinceBuildOrder.objects.get(got=entry)

    otype, olvl = pp.ppresence.getPair(pp.slot)
    if otype != 0:
        pp.ppresence.setPair(pp.slot, pp.what, olvl+1)
    else:
        pp.ppresence.setPair(pp.slot, pp.what, 1)

    pp.ppresence.save()
    
    if pp.what in (1,2,3):
        recalc(pp.ppresence.owner)

    pp.delete()  
    
def cancelBuild(ppresence, slot):
    mbo, = ProvinceBuildOrder.objects.filter(ppresence=ppresence).filter(slot=slot)
    mbo.got.delete()
    x = mbo.what
    mbo.delete()
    return x
    
def orderBuild(ppresence, mother, what, slot, costs):
    mother.owner.resources.stateUpdate()
    mother.owner.resources -= costs[0]
    mother.owner.resources.save()  
    note(mother.owner.id, costs[0], 'province')
    willFinish = datetime.fromtimestamp(int(costs[1] + time()))
    got = GenericOrderTable(None,
                            willFinish,
                            datetime.now(),
                            3)
    got.save()
    mbo = ProvinceBuildOrder(None,
                             got.id,
                             ppresence.id,
                             what,
                             slot,
                             )
    mbo.save()