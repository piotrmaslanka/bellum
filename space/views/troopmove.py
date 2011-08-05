# coding=UTF-8
from django.shortcuts import redirect
from bellum.common.alliance import isAllied
from bellum.common.session.login import must_be_logged
from bellum.common.session import getAccount, getRace
from bellum.common.session.mother import getCurrentMother
from djangomako.shortcuts import render_to_response, render_to_string
from bellum.space.models import Planet
from bellum.common.gui import PrimaryGUIObject
from bellum.common.fixtures.province_build import getCosts
from bellum.common.session import getRace, getAccount, getResourceIndex
from bellum.landarmy.models import Garrison
from bellum.meta import MPBI, MGI
from bellum.province.models import Province, Reinforcement
from django.core.exceptions import ObjectDoesNotExist
from bellum.province.models import ProvintionalPresence, Reinforcement
from bellum.space.ajax.tdinfo import p_plm, p_garrison_prov_dx, p_commands
from bellum.orders.mother.landarmy_mpickup import orderMotherPickup, orderReinforcementsPickup
from bellum.orders.models import LandarmyPlanetaryStrikeOrder, LandarmyProvintionalStrikeOrder
from bellum.orders.province.landarmy_pstrike import orderProvintionalStrike
from bellum.orders.mother.landarmy_mdrop import orderPlanetaryStrike
from bellum.stats.larf.const import LP_DEPLOY_LAND_GROUND, LP_MOTHER_PICKUP_LAND, LM_DEPLOY_LAND_GROUND
from bellum.stats.larf import note
from bellum.common.utils import STRIKEORDER_DESIGNATION # list of designations
from django.http import HttpResponse

def generate(request, mother=None, current_province=None, highlight=None):
    '''highlight is either None (highlight mother) or True (highlight province)'''

    account = getAccount(request)
    if mother == None: mother = getCurrentMother(request)

    # let's ascertain two variables that will be the basis of functioning of this script.
    # @current_planet is a bellum.space.models.Planet instance, and is the planet which map we are rendering
    # @current_province(parameter) is a bellum.province.models.Province instance, and is the province which is highlighted

    if current_province == None:    # if none, then use mothership
        current_planet = mother.duePosition()        # we do not need to highlight a province as it is mother hq we're operating on
        highlight_planet = False
    else:
        highlight_planet = True
        current_planet = current_province.planet
        if current_province.presence.owner != account:
            try:
                current_province.presence.reinforcement_set.get(owner=account)
            except ObjectDoesNotExist:
                return redirect('/')    # You can't choose a province that's neither yours nor you have reinforcements on

    # --------------------------------   Construct planet list
    presences = ProvintionalPresence.objects.filter(owner=account)  # Get all my provinces

    planets = []
    provinces_per_planet = {}
    for presence in presences:
        if not presence.province.planet in planets: planets.append(presence.province.planet)
        try:
            provinces_per_planet[presence.province.planet.id] += 1
        except KeyError:
            provinces_per_planet[presence.province.planet.id] = 1

    reinfs = Reinforcement.objects.filter(owner=account)
    for reinf in reinfs:
        if not reinf.presence.province.planet in planets: planets.append(reinf.presence.province.planet)
        try:
            provinces_per_planet[reinf.presence.province.planet.id] += 1
        except KeyError:
            provinces_per_planet[reinf.presence.province.planet.id] = 1

    limit_cmdr = False

    # ----------------------------------    Construct garrison

    if current_province == None:
        garrison = mother.garrison
    else:
        if current_province.presence.owner == account:
            garrison = current_province.presence.garrison
        else:
            limit_cmdr = True
            garrison = current_province.presence.reinforcement_set.get(owner=account).garrison

    return render_to_response('space/troopmove/base.html', {'pgo':PrimaryGUIObject(request),
                                                            'planets':planets,
                                                            'mother':mother,
                                                            'highlight_planet':highlight_planet,
                                                            'current_planet':current_planet,
                                                            'current_province':current_province,
                                                            'provinces_per_planet':provinces_per_planet,
                                                            'fillin_pla':p_plm(request, current_planet, highlight_preference=current_province).decode('utf8'),
                                                            'fillin_garrison':p_garrison_prov_dx(request, garrison, getRace(request)).decode('utf8'),
                                                            'fillin_commands':p_commands(request, current_planet, current_province, limit_cmdr).decode('utf8')})


from bellum.orders.models import LandarmyPlanetaryStrikeOrder, LandarmyProvintionalStrikeOrder

def cancel_drop(request):
    '''cancels a drop of drop ID given as GET id'''
    try:
        lpso = LandarmyPlanetaryStrikeOrder.objects.get(id=int(request.GET['id']))
    except:
        return HttpResponse('FAIL')
    if lpso.designation == 0: return HttpResponse('FAIL')
    if lpso.mother.owner != getAccount(request): return HttpResponse('FAIL')
    lpso.fallback()
    return HttpResponse('OKAY')

def cancel_strike(request):
    '''cancels a provintional strike of ID given as GET id'''
    try:
        lpso = LandarmyProvintionalStrikeOrder.objects.get(id=int(request.GET['id']))
    except:
        return HttpResponse('FAIL')
    if lpso.designation == 0: return HttpResponse('FAIL')
    if lpso.attacker != getAccount(request): return HttpResponse('FAIL')
    lpso.directiveFallback()
    return HttpResponse('OKAY')



# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> ENTRY POINTS
@must_be_logged
def dxmother(request):
    return generate(request)

@must_be_logged
def dxprovince(request, province_id):
    try:
        prov = Province.objects.get(id=province_id)
    except:
        return redirect('/')
    return generate(request, current_province=prov, highlight=True)


@must_be_logged
def submit(request):
    '''The great submit procedure. Accepts nearby anything, and has to resolve it to make sense.
    And BTW it has to send troops'''
    # MEMO: If an error occurs here, it kills the script, preventing it from doing anything. It's a GOOD thing, a DEFENSE against
    # the user. User won't notice, because this script handles AJAX, and AJAX is processed by my JavaScript, not by browser
    # Quite a show off code it is, isn't it?
    # --------------------------------------    grab designation, and substitute it for valid in-game code
    designation = int(request.GET['designation'])
    if not (designation in (0,1,2)): return HttpResponse('HACK')    # Prevent invalid designations
    dmap = {0:2, 1:1, 2:3}  # true code for JS 0 is 2 ("Attack")
                            # true code for JS 1 is 1 ("Attack if not allied on arrival, else Reinforce")
                            # true code for JS 2 is 3 ("Fallback if not allied on arrival, else Reinforce")
                            # there are also other designations(0 - I'm falling back, 4 - Reinforce, 5 - Fallback on arrival)
                            # there are either old or debug
    designation = dmap[designation]
    # --------------------------------------    Try to ascertain what we are actually doing. And there's lotta of possibilities
    source = request.GET['source']
    target = request.GET['target']
    if (source == 'null') and (target == 'null'): raise Exception # Situation where mother is both source and target are right out
    if source == 'null':        # We are dropping stuff from mothership
        mother = getCurrentMother(request)      # Get our mother object
        target = Province.objects.get(id=int(target))    # In that case we are dropping unto a province
        if target.planet != mother.duePosition(): return HttpResponse('HQNT') # Mother cannot drop to a province - she's not there
        if mother.isRelocating(): return HttpResponse('RELOC')                  # Mother can't drop during a relocation
        # Ok, I see no reasons why we shoudn't perform the action for now.
        order = 'DROP'
        src_garrison = mother.garrison  # Store mother garrison for further checking and reference
    elif target == 'null':      # We are evacuating
        mother = getCurrentMother(request)      # Get our mother object
        source = Province.objects.get(id=int(source))    # Get our province object
        if source.planet != mother.duePosition(): return HttpResponse('HQNT')  # Mother cannot evac from a province - she's not there
        if mother.isRelocating(): return HttpResponse('RELOC')                  # Mother can't evac during a relocation
        if source.presence.owner != getAccount(request):    # If province is not ours (if it's unoccupied, error happens)
            reinf = source.presence.reinforcement_set.get(owner=getAccount(request))    # If we don't have any reinforcements, error happens
            order = 'EVAC-REINF'    # Ok, we can evacuate our reinforcements
            src_garrison = reinf.garrison  # Store reinforcement garrison for further checking and reference
        else:
            order = 'EVAC'  # Evacuate our units
            src_garrison = source.presence.garrison  # Store provintional garrison for further checking and reference
    else:       # We are doing a province-to-province transfer
        source = Province.objects.get(id=int(source))
        target = Province.objects.get(id=int(target))

        if source.planet != target.planet: raise Exception      # Obviously, you can't make interplanetary transfers here :D
        if source.presence.owner != getAccount(request): return HttpResponse('HACK')   # Can't comandeer a province that's not mine. Unoccupied - error
        if not (target in source.getNeighbours()): return HttpResponse('HACK')       # Must be a neighbouring province
        # Ok, no reasons why we shouldn't do it
        order = 'ATTACK'
        src_garrison = source.presence.garrison  # Store provintional garrison for further checking and reference
    # --------------------------------------    Reconstruct a garrison object from that JavaScript GET babble
    garrison = Garrison()
    for i in xrange(0, MGI+1):          # Do that for every possible troop type
        try:
            gv = int(request.GET['st'+str(i)])   # Try to get troop number of troop type "i" from JavaScript GET
        except:         # If it's not there...
            gv = 0       # Ignore the error. There might be more units ahead to read.
        garrison[i] = gv      # Store the value unto garrison
        i += 1      # Increase i
    # -------------------------------------    Check whether we can send that many troops
    if garrison.isZero(): return HttpResponse('ZERO')       # You want to send 0 units? How could it be...
    if not (garrison in src_garrison): return HttpResponse('HACK')
    # -------------------------------------    Being outfitted with knowledge of what to do, and with that to do that, let's do that ;)
                                # In each case, we will list variables that are already ready to use.
    if order == 'EVAC':     # Process evacuation request
        orderMotherPickup(source.presence, garrison, mother, race=getRace(request))    # Order the evacuation
        note(request, LP_MOTHER_PICKUP_LAND, pid=source.id,
                                             garrison=garrison,
                                             mid=mother.id)     # Store info about evacuation to last-done-stuff(LARF, ie. Last Actions Reporting Format)
    elif order == 'EVAC-REINF': # Process reinforcement evacuation request
        orderReinforcementsPickup(source.presence, garrison, mother, reinf, race=getRace(request))
        note(request, LP_MOTHER_PICKUP_LAND, pid=source.id,
                                         garrison=garrison,
                                         mid=mother.id)         # Save info about pickup into LARF
    elif order == 'DROP':    # Process drop request
        orderPlanetaryStrike(garrison, mother, target, designation, 0, race=getRace(request))
                                                                          # order the drop
                                                                          # Last zero parameter is a placeholder to additional commands
                                                                          # if these were to be implemented at some point in-game
        note(request, LM_DEPLOY_LAND_GROUND, mid=mother.id,
                                             garrison=garrison,
                                             provinceid=target.id,
                                             designation=designation,
                                             orders=0)                  # Save info into LARF
    elif order == 'ATTACK':     # Process province-to-province transfers
        orderProvintionalStrike(garrison, source, target, designation, 0, race=getRace(request))   # Order the strike
        note(request, LP_DEPLOY_LAND_GROUND, pid=source.id,
                                             garrison=garrison,
                                             target=target,
                                             designation=designation,
                                             orders=0)      # Store info about the deployment into LARF
    else:
        # Something terrible, terrible has happened. We are processing unknown order, or our code took an exceptionally wrong codepath.
        # It's so terrible it's disgusting. And it's totally my fault. If something like that happens, I should fix it ASAP.
        raise Exception
    return HttpResponse('OK')       # Signal that stuff went just OK