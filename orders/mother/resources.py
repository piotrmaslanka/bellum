from bellum.orders.models import ResourceSendOrder, GenericOrderTable
from time import time
from datetime import datetime, timedelta
from bellum.common.models import ResourceIndex
from bellum.common.fixtures.resources import getResourceTravelTime
from bellum.stats.igstatistics.resources_sent import note
from bellum.stats.larf import note
from bellum.stats.larf.const import LM_RCVD_RESOURCE

def cancelResourceSend(resourceSendInstance):
    '''cancels a resource send. Does not return resources'''
    resourceSendInstance.got.delete()
    resourceSendInstance.delete()

def orderResourceSend(mother_from, mother_to, titan, pluton, men):
  '''orders a resource send'''  
  got = GenericOrderTable(None,
                          datetime.now()+timedelta(0, getResourceTravelTime(mother_from, mother_to)),
                          datetime.now(),
                          4)
  got.save()
  mbo = ResourceSendOrder(None,
                          got.id,
                          titan, pluton, men,
                          mother_to.id,
                          mother_from.id)
  mbo.save()

 
  rindex = mother_from.owner.resources
  rindex -= ResourceIndex(titan=titan, pluton=pluton, men=men)
  rindex.save()
  note(mother_from.owner.id, ResourceIndex(titan=titan, pluton=pluton, men=men), 'sent')
  
  
def doResourceSendOrder(entry):
    mob = ResourceSendOrder.objects.get(got=entry)
    rsTuple = ResourceIndex(titan=mob.titan, pluton=mob.pluton, men=mob.men)
    
    targetResourceIndex = mob.send_to.owner.resources
    targetResourceIndex += rsTuple
    
    targetResourceIndex.save()

    note(None, LM_RCVD_RESOURCE, mfrom=mob.send_from,
                                 target=mob.send_to,
                                 resources=rsTuple)
    
    mob.delete()
    
def performTradeOffer(entry, secmum):
    '''entry is a mother.models.TradeOffer. secmum is mother of player who accepts the offer.
    Assumes player has enuff resources'''

    fp = entry.owner.resources
    fp += ResourceIndex(titan=entry.titan_p, pluton=entry.pluton_p, men=entry.men_p)
    fp.save()

    orderResourceSend(entry.mother, secmum, entry.titan_p, entry.pluton_p, entry.men_p)
    orderResourceSend(secmum, entry.mother, entry.titan_f, entry.pluton_f, entry.men_f)
    
    
    
