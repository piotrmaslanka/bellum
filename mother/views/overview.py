# coding=UTF-8
from django.shortcuts import redirect
from djangomako.shortcuts import render_to_response
from bellum.common.session.login import must_be_logged
from bellum.common.session import getRace, getTechnology
from bellum.common.session.mother import getCurrentMother
from bellum.common.fixtures import mother_construction
from bellum.common.fixtures import technology
from bellum.common.gui import PrimaryGUIObject
from bellum.orders.models import MotherRelocationOrder, LandarmyMotherPickupOrder, LandarmyPlanetaryStrikeOrder

@must_be_logged
def process(request):
    mum = getCurrentMother(request)
    tech = getTechnology(request)

    try:
        mro, = MotherRelocationOrder.objects.filter(mother=mum)
    except:
        relocating = False
        mro = None
    else:
        relocating = True
    constructions = mum.getConstructions()
    researches = mum.getResearches()

    return render_to_response('mother/overview/overview.html', {'mother':mum,
                                                                'constructions':constructions,
                                                                'c_requirements':mother_construction.getRequirementsArray(mum, getRace(request)),
                                                                'c_costs':mother_construction.getCostsArray(mum, getRace(request)),
                                                                'technology':tech,
                                                                'researches':researches,
                                                                't_costs':technology.getCostsArray(tech, getRace(request)),
                                                                't_requirements':technology.getRequirementsArray(tech, getRace(request)),
                                                                'pgo':PrimaryGUIObject(request),
                                                                'relocating':relocating,
                                                                'mro':mro,
                                                                'race':getRace(request),
                                                                })
