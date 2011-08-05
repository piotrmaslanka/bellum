from __future__ import division
from math import ceil
from djangomako.shortcuts import render_to_response
from bellum.common.session.login import must_be_logged
from django.shortcuts import redirect
from bellum.common.session import getAccount

from bellum.common.gui import PrimaryGUIObject
from bellum.stats.models import RankingNone, RankingArmy, RankingMother, RankingAlliance

RPP = 10

@must_be_logged
def process(request, rankingtype, page):
    if not (rankingtype in ('all', 'mother', 'army', 'allied')):
            return redirect('/')

    rt = {'all':RankingNone, 'army':RankingArmy, 'mother':RankingMother, 'allied':RankingAlliance}

    if page == None:
        # caveats
        pass
    else:
        page = int(page)
        ranking = rt[rankingtype].objects.filter(id__gt=RPP*(page-1)).filter(id__lt=(RPP*page)+1)

    acc = getAccount(request)

    total_objects_count = rt[rankingtype].objects.count()
    pages = int(ceil(total_objects_count / RPP))

    pagination = []

    if (pages < 8):      # special case - static
        pagination = range(1, pages+1)
    elif (page > 3) and (page < pages-2):     # no special cases apply
        pagination = [page-3, page-2, page-1, page, page+1, page+2, page+3]
    elif (page < 4):    # less than 3 entries left
        pagination = range(1, page+1) + [page+1, page+2, page+3]
    elif (page > pages-4):      # less than 3 entries right
        pagination = [page-3, page-2, page-1, page] + range(page+1, pages+1)

    return render_to_response('stats/ranking/'+rankingtype+'.html',{'pgo':PrimaryGUIObject(request),
                                                                    'account':acc,
                                                                    'page':page,
                                                                    'pagecount':pages,
                                                                    'pages':pagination,
                                                                    'ranking':ranking})



