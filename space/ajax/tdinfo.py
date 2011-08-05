from djangomako.shortcuts import render_to_string
from bellum.common.session.login import must_be_logged
from bellum.common.session import getAccount, getRace
from bellum.common.gui import PrimaryGUIObject
from bellum.province.models import Province, Reinforcement
from bellum.common.session.mother import getCurrentMother
from bellum.common.fixtures.province_build import getCosts
from bellum.meta import MPBI
from django.core.exceptions import ObjectDoesNotExist
from bellum.space.ajax import p_available
from bellum.orders.models import LandarmyProvintionalStrikeOrder
from bellum.orders.models import LandarmyPlanetaryStrikeOrder, LandarmyProvintionalStrikeOrder, LandarmyMotherPickupOrder
from django.http import HttpResponse
from bellum.space.models import Planet
from bellum.common.alliance import isAllied
from json import dumps

def p_plm(request, planet, highlight_preference=None):
    '''Generate planet map
    highlight preference is a province instance'''
    allegiance_tab = {}
    for province in planet.province_set.all():
        # 0 - MINE, 1 - ENEMY, 2 - ALLIED, 3 - NOBODYS
        try:
            province.provintionalpresence
        except:
           allegiance_tab[province.id] = 'gray'
        else:
            if province.provintionalpresence.owner == getAccount(request):
                allegiance_tab[province.id] = 'green'
            elif isAllied(getAccount(request), province.provintionalpresence.owner):
                allegiance_tab[province.id] = 'blue'
            else:
                allegiance_tab[province.id] = 'red'

    x = render_to_string('space/troopmove/generator/pla.html', {'planet':planet,
                                                                'wctg':lambda x: int((x+100.0)*(345.0/200.0)),
                                                                'allegiance_strings':allegiance_tab,
                                                                'highlight_preference':highlight_preference})
    return x


def p_garrison_prov_dx(request, garrison, race):
    '''Directly provides with garrison HTML. Unfortunately, by being direct, it is also quite dumb'''
    return render_to_string('space/troopmove/generator/garrison.html', {'garrison':garrison,
                                                                        'race':race})

def p_commands(request, planet, source, reinforcements=False):
    '''Source is either None(mothership) or a bellum.province.models.Province instance.
    If reinforcements, then severely limit commandeering capability'''
    return render_to_string('space/troopmove/generator/commands.html', {'display_mother':source!=None,
                                                                        'source':source,
                                                                        'mother':getCurrentMother(request),
                                                                        'planet':planet,
                                                                        'limit_comandeering':reinforcements})


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> ENTRY POINTS ( DXInterface for AJAX )

@must_be_logged
def planetpick_planet(request, planet_id):
    '''We have picked a planet. That implies generating everything new.
    Returns a tuple in JSON:
        - PLM (HTML)
        - garrison (HTML)
        - commands (HTML)
        - new CurrentPlanetID
        - new SelectedProvince'''

    try:
        planet = Planet.objects.get(id=planet_id)
    except ObjectDoesNotExist:
        return HttpResponse(dumps(None))

    account = getAccount(request)

    current_province = None
    current_garrison = None
    current_planet = planet
    allowDisplay = False
    limit_cmdr = False

    for province in planet.province_set.all():
        try:
            province.presence
        except:
            continue
        if province.presence.owner == account:
            allowDisplay = True
            if current_province == None: current_province = province
            current_garrison = province.presence.garrison
            break
        try:
            reinf = province.presence.reinforcement_set.get(owner=account)
        except ObjectDoesNotExist:
            continue
        else:
            # We have reinforcements there
            allowDisplay = True
            current_province = province
            current_garrison = reinf.garrison
            limit_cmdr = True
            break

    if not allowDisplay: return HttpResponse('INVALIDPLANET')

    plm = p_plm(request, planet, highlight_preference=current_province)
    plg = p_garrison_prov_dx(request, current_garrison, getRace(request))
    plc = p_commands(request, current_planet, current_province, limit_cmdr)

    repl = dumps((plm, plg, plc, current_planet.id, current_province.id))
    return HttpResponse(repl)

@must_be_logged
def planetpick_mother(request):
    '''We have picked a mothership. That implies generating everything new.
    Returns a tuple in JSON:
        - PLM (HTML)
        - garrison (HTML)
        - commands (HTML)
        - new CurrentPlanetID'''

    mother = getCurrentMother(request)
    planet = mother.duePosition()
    plm = p_plm(request, planet)
    plg = p_garrison_prov_dx(request, mother.garrison, getRace(request))
    plc = p_commands(request, mother.duePosition(), None)

    repl = dumps((plm, plg, plc, mother.duePosition().id))

    return HttpResponse(repl)


@must_be_logged
@p_available
def provincepick(request, province):
    '''Returns a tuple in JSON:
        - garrison (HTML)
        - commands (HTML)
        - province's planet_count_number'''

    account = getAccount(request)
    # deem whether the user can access this
    try:
        province.presence           # Must be inhabited
    except:
        return HttpResponse(dumps(None))


    if province.presence.owner != account:  # if not mine...
        try:
            reinf = province.presence.reinforcement_set.get(owner=account)
        except ObjectDoesNotExist:
            return HttpResponse(dumps(None))    # I don't have even reinforcements here
                                                # Get me outta here!
        # However if I have reinforcements here, then it's different
        garrison = reinf.garrison
        reinforcements = True
    else:   # is mine
        garrison = province.presence.garrison
        reinforcements = False

    garr = p_garrison_prov_dx(request, garrison, getRace(request))
    comms = p_commands(request, province.planet, province, reinforcements)

    x = dumps((garr, comms, province.planet_count_number))
    return HttpResponse(x)