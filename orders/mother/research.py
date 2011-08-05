from bellum.orders.models import TechnologyResearchOrder, GenericOrderTable
from time import time
from datetime import datetime
from bellum.stats.igstatistics.resources_sent import note

def cancelResearch(technologyInstance):
    technologyInstance.got.delete()
    technologyInstance.delete()

def orderResearch(mother, what, costs):
  '''orders a research. Costs are expected to be an tuple with:
        unbound bellum.common.models.ResourceIndex instance
        integer item representing build length in seconds'''  
    
  mother.owner.resources.stateUpdate()
  mother.owner.resources -= costs[0]
  mother.owner.resources.save()

  note(mother.owner.id, costs[0], 'research')

  willFinish = datetime.fromtimestamp(int(costs[1] + time()))
  got = GenericOrderTable(None,
                          willFinish,
                          datetime.now(),
                          2)
  got.save()
  mbo = TechnologyResearchOrder(None,
                            got.id,
                            what,
                            mother.id)
  mbo.save()
  


def doTechnologyResearchOrder(entry):
    mbo = TechnologyResearchOrder.objects.get(got=entry)
    tech = mbo.mother.owner.technology
    
    tech.setTechnologyLevelById(mbo.what, tech.getTechnologyLevelById(mbo.what) + 1)
    tech.save()
    
    if (mbo.what == 2) or (mbo.what == 3):
        from bellum.common.fixtures.resources import recalc
        recalc(mbo.mother.owner)
        
    mbo.delete()
        
