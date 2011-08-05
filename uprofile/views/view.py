from django.shortcuts import redirect
from djangomako.shortcuts import render_to_response
from bellum.register.models import Account
from bellum.common.session.login import must_be_logged
from bellum.common.gui import PrimaryGUIObject
from bellum.common.session import getAccount
from bellum.common.fixtures.resources import getResourceTravelTime
from bellum.common.session.mother import getCurrentMother
from bellum.mother.models import Mother

@must_be_logged
def process(request, acc_id):
    try:
        acc = Account.objects.get(id=acc_id)
    except:
        return redirect('/')

    try:
        tmum = Mother.objects.get(owner=acc)
    except:
        # unregistered
        return redirect('/stats/empire/')

    rtt = getResourceTravelTime(getCurrentMother(request), tmum)

    return render_to_response('uprofile/view/view.html', {'account':acc,
                                                          'rtt':rtt,
                                                          'same': getAccount(request) == acc,
                                                          'pgo':PrimaryGUIObject(request)})
    
