from bellum.orders.models import MotherConstructionOrder, GenericOrderTable
from time import time
from datetime import datetime
from bellum.stats.igstatistics.resources_sent import note

def cancelConstruct(mcoInstance):
    mcoInstance.got.delete()
    mcoInstance.delete()

def orderConstruct(mother, what, costs):
  '''orders a build. Costs are expected to be an tuple with:
        unbound bellum.common.models.ResourceIndex instance
        integer item representing build length in seconds'''  
  mother.owner.resources.stateUpdate()
  mother.owner.resources -= costs[0]
  mother.owner.resources.save()
  note(mother.owner.id, costs[0], 'mother')
    
  willFinish = datetime.fromtimestamp(int(costs[1] + time()))
  got = GenericOrderTable(None,
                          willFinish,
                          datetime.now(),
                          1)
  got.save()
  mbo = MotherConstructionOrder(None,
                            got.id,
                            what,
                            mother.id
                            )
  mbo.save()
  


def doMotherConstructOrder(entry):
    mbo = MotherConstructionOrder.objects.get(got=entry)
    mum = mbo.mother
    
    mum.setConstructionLevelById(mbo.what, mum.getConstructionLevelById(mbo.what) + 1)
    mum.save()

    if mbo.what in (1,2):           # enlarged Dust Collector or Quarters
        from bellum.common.fixtures.resources import recalc
        recalc(mum.owner)
        
    mbo.delete()
        
