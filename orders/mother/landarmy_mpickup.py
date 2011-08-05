from __future__ import division
from bellum.orders.models import LandarmyMotherPickupOrder, GenericOrderTable
from time import time
from datetime import datetime, timedelta
from bellum.landarmy.models import Garrison
from bellum.common.utils import timedelta__seconds
from bellum.common.fixtures.landarmy_relocate import pmmovelen

def orderReinforcementsPickup(presence, garrison, mother, reinforcement, race=None):
    reinforcement.garrison -= garrison

    if reinforcement.garrison.isZero():
        reinforcement.garrison.delete()
        reinforcement.delete()
    else:
        reinforcement.garrison.save()

    garrison.save()

    willFinish = datetime.fromtimestamp(int(pmmovelen(presence.province, mother, garrison, race=race) + time()))
    got = GenericOrderTable(None,
                            willFinish,
                            datetime.now(),
                            8)
    got.save()

    lmpo = LandarmyMotherPickupOrder(None,
                                     got.id,
                                     mother.id,
                                     presence.province.id,
                                     garrison.id)
    lmpo.save()


def orderMotherPickup(presence, garrison, mother, race=None):
    presence.garrison -= garrison
    presence.garrison.save()
    garrison.save()
    
    willFinish = datetime.fromtimestamp(int(pmmovelen(presence.province, mother, garrison, race=race) + time()))
    got = GenericOrderTable(None,
                            willFinish,
                            datetime.now(),
                            8)    
    got.save()
    
    lmpo = LandarmyMotherPickupOrder(None,
                                     got.id,
                                     mother.id,
                                     presence.province.id,
                                     garrison.id)
    lmpo.save()


def doLandarmyMotherPickupOrder(entry):
    lmpo = LandarmyMotherPickupOrder.objects.get(got=entry)
    gar = lmpo.garrison
    
    lmpo.mother.garrison += gar
    lmpo.mother.garrison.save()

    lmpo.delete()
    gar.delete()
    