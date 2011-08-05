from djangomako.shortcuts import render_to_response
from bellum.common.session.login import must_be_logged
from bellum.common.session import getAccount
from bellum.common.gui import PrimaryGUIObject
from bellum.stats.larf.storage import fileFor

@must_be_logged
def process(request):
    acc = getAccount(request)

    ll = fileFor(acc.id)

    a = []
    tmp = []
    for x in ll.readlines():
        tmp += [x]
        if len(tmp) == 2:       # should be appended
            a.append(tmp)
            tmp = []

    return render_to_response('stats/larf/larf.html',{'pgo':PrimaryGUIObject(request),
                                                      'entries':a})