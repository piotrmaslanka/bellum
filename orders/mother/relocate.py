from time import time
from datetime import datetime, timedelta
from bellum.orders.models import GenericOrderTable, MotherRelocationOrder, LandarmyProduceOrder
from bellum.common.fixtures.relocation import getRelocationTime 

def orderRelocate(mother, race, target_planet):
    now = time()
    relTime = getRelocationTime(mother, race, mother.orbiting, target_planet)
    completion = now + relTime

    
    got = GenericOrderTable(None,
                            datetime.fromtimestamp(completion),
                            datetime.fromtimestamp(now),
                            0)
    got.save()

    
    
    mro = MotherRelocationOrder(None,
                                got.id,
                                mother.orbiting.id,
                                target_planet.id,
                                mother.id)
    mro.save()
    
def doRelocationOrder(entry):
    mro, = MotherRelocationOrder.objects.filter(got=entry)
    mum = mro.mother
    mum.orbiting = mro.loc_to
    mum.save()
    mro.delete()
    
