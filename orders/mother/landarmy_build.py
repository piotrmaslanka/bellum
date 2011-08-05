from __future__ import division
from bellum.orders.models import LandarmyProduceOrder, GenericOrderTable
from time import time
from datetime import datetime, timedelta
from bellum.common.fixtures.landarmy_produce import getCosts
from bellum.landarmy.models import Garrison
from bellum.orders import DontRemoveGOT
from bellum.common.utils import timedelta__seconds
from bellum.stats.igstatistics.resources_sent import note

def orderProduce(mother, race, what, amount):
  '''orders a production. Costs are expected to be an tuple with:
        unbound bellum.common.models.ResourceIndex instance
        integer item representing build length in seconds'''
        
  mother.owner.resources.stateUpdate()
  
  cost_res, ctime = getCosts(mother, race, what)
  cost_res *= amount
  
  mother.owner.resources -= cost_res
  mother.owner.resources.save()
  note(mother.owner.id, cost_res, 'landarmy')

  try:
      lpmax = LandarmyProduceOrder.objects.filter(mother=mother.id).order_by('-got__ordered_on')[0]
  except:
      subfox = datetime.now()
  else:
      subfox = lpmax.got.ordered_on + timedelta(0, lpmax.maketime * lpmax.amount)
    
  got = GenericOrderTable(None,
                          subfox + timedelta(0, ctime),
                          subfox,
                          5)
  got.save()
  lpo = LandarmyProduceOrder(None,
                             got.id,
                             mother.id,
                             what,
                             amount,
                             ctime
                             )
  lpo.save()
  


def doLandarmyProduceOrder(entry):
    lpo = LandarmyProduceOrder.objects.get(got=entry)
    gar = lpo.mother.garrison
    now = datetime.now()

    interval = timedelta__seconds(now - entry.ordered_on)
    soldiers = interval // lpo.maketime      # it is important that we use integral division
    csmktime = soldiers*lpo.maketime        # how long did soldiers made in this turn take to do?
    if soldiers > lpo.amount:
        soldiers = lpo.amount
    
    gar.__dict__['st'+str(lpo.sold_nr)] += soldiers    
    gar.save()

    lpo.amount -= soldiers

    if lpo.amount == 0:
        lpo.delete()
    else:
        entry.ordered_on += timedelta(0, csmktime)
        entry.to_be_completed = entry.ordered_on + timedelta(0, lpo.maketime)
        lpo.save()
        entry.save()
        raise DontRemoveGOT