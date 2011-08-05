#from random import random
from django.db import connection
from datetime import datetime
from bellum.orders.mother.relocate import doRelocationOrder
from bellum.orders.mother.construct import doMotherConstructOrder
from bellum.orders.province.build import doProvinceBuildOrder
from bellum.orders.mother.research import doTechnologyResearchOrder
from bellum.orders.mother.resources import doResourceSendOrder
from bellum.orders.mother.landarmy_build import doLandarmyProduceOrder
from bellum.orders.mother.landarmy_mpickup import doLandarmyMotherPickupOrder
from bellum.orders.mother.landarmy_mdrop import doLandarmyPlanetaryStrikeOrder
from bellum.orders.province.landarmy_pstrike import doLandarmyProvintionalStrikeOrder
from bellum.orders.models import GenericOrderTable
from bellum.orders import DontRemoveGOT
from django.db import connection

def runSite():
    cursor = connection.cursor()
    cursor.execute('LOCK TABLES chat_lcdmessage WRITE, stats_report WRITE, orders_genericordertable WRITE, common_resourceindex WRITE, landarmy_garrison WRITE, mother_mother WRITE, mother_technology WRITE, orders_landarmymotherpickuporder WRITE, orders_landarmyplanetarystrikeorder WRITE, orders_landarmyproduceorder WRITE, orders_landarmyprovintionalstrikeorder WRITE, orders_motherconstructionorder WRITE, orders_motherrelocationorder WRITE, orders_provincebuildorder WRITE, orders_resourcesendorder WRITE, orders_technologyresearchorder WRITE, province_provintionalpresence WRITE, province_reinforcement WRITE, register_account READ, alliance_alliance READ, alliance_alliancemembership READ, space_planet READ, province_province READ')
    
    gotentries = GenericOrderTable.objects.filter(to_be_completed__lte=datetime.now()).order_by('to_be_completed')

    for entry in gotentries:
        try:
            if entry.ordertype == 0:
                doRelocationOrder(entry)
            if entry.ordertype == 1:
                doMotherConstructOrder(entry)
            if entry.ordertype == 2:
                doTechnologyResearchOrder(entry)
            if entry.ordertype == 3:
                doProvinceBuildOrder(entry)
            if entry.ordertype == 4:
                doResourceSendOrder(entry)
            if entry.ordertype == 5:
                doLandarmyProduceOrder(entry)
            if entry.ordertype == 6:
                doLandarmyPlanetaryStrikeOrder(entry)
            if entry.ordertype == 7:
                doLandarmyProvintionalStrikeOrder(entry)
            if entry.ordertype == 8:
                doLandarmyMotherPickupOrder(entry)
        except DontRemoveGOT:
            pass
        else:
            entry.delete()

    cursor.execute('UNLOCK TABLES')
            
class OrderMiddleware(object):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.META['PATH_INFO'][:6] != '/chat/': # Don't invoke middleware on chat operations
                                                       # because the overhead would fuck the DB
            runSite()
        return None
