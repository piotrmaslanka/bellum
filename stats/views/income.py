from djangomako.shortcuts import render_to_response
from bellum.common.session.login import must_be_logged
from bellum.common.session import getAccount
from bellum.province.models import ProvintionalPresence
from bellum.mother.models import Mother
from bellum.common.gui import PrimaryGUIObject
from bellum.common.models import ResourceIndex
from bellum.common.fixtures.resources.recalculate import calculate_presence, calculate_mother

@must_be_logged
def process(request):
    acc = getAccount(request)

    # cash_data: dict{planet_id => list( ... (province_id, province_name, cash) ... ) }
    # planetary_map: dict(planet_id => planet_name)
    # sumup_data: dict(planet_id => sum_of_incomes)
    # ppres: set of analyzed presences
    cash_data = {}
    planetary_map = {}
    ppres = ProvintionalPresence.objects.filter(owner=acc)
    sumup_data = {}

    for pp in ppres:
        try:        # Cache in mapping
            planetary_map[pp.province.planet_id]
        except:
            planetary_map[pp.province.planet_id] = pp.province.planet.name

        try:        # Ensure a cash_data slot exists
            cash_data[pp.province.planet_id]
        except:
            cash_data[pp.province.planet_id] = []

        try:        # Ensure a sumup_data slot exists
            sumup_data[pp.province.planet_id]
        except:
            sumup_data[pp.province.planet_id] = ResourceIndex()

        cp = calculate_presence(pp)
        cash_data[pp.province.planet_id].append((pp.province_id, pp.province.name, cp))
        sumup_data[pp.province.planet_id].addRatio(cp)
       
    mother = Mother.objects.get(owner=acc)
    mum = calculate_mother(mother)
    
    return render_to_response('stats/income/income.html',{'pgo':PrimaryGUIObject(request),
                                                          'account':acc,
                                                          'provinces':cash_data,
                                                          'planet_sums':sumup_data,
                                                          'planet_id_to_name':planetary_map,
                                                          'mother':mum,
                                                          'zero':zero,
                                                          'mother_name':mother.name})
def zero(x):
    x = int(x)
    if x == 0:
        return '<span class="zero">'+str(x)+'</span>'
    else:
        return str(x)
