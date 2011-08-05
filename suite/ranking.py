from bellum.stats.models import RankingNone, RankingMother, RankingArmy, RankingAlliance
from bellum.register.models import Account
from bellum.alliance.models import Alliance, AllianceMembership
from django.db import connection
from bellum.stats import IGSTATISTICS

def read_resources(acc_list):
    mod = {}
    for acc in acc_list:
        try:
            mod[acc.id] = eval(open(IGSTATISTICS+'rs'+str(acc.id), 'r').read())
        except:
            None    # they just won't get processed and appended to list
    return mod


def ranking_against_ids(ranks):
    mod = {}
    for ranking in ranks:
        mod[ranking.account_id] = ranking.id
    return mod

def regen_personal_ranking_none():
    rnkn = ranking_against_ids(RankingNone.objects.all())
    ress = read_resources(Account.objects.all())
            # interchange this part
    score = []          # score is a list of tuples(accid, score)
    for accid, resdict in ress.iteritems():
        try:
            score.append((accid, resdict[None][0] + resdict[None][1] + resdict[None][2]))
        except:
            score.append((accid, 0))
            # score counting done
    score = sorted(score, key=lambda k: k[1], reverse=True)
    cursor = connection.cursor()
    cursor.execute("TRUNCATE TABLE stats_rankingnone")      # pwn the table

    nrid = 1
    for accid, pts in score:
        acc = Account.objects.get(id=accid)
        try:
            am = AllianceMembership.objects.get(account=acc)
        except:
            # not allied
            shname = ''
            allid = 0
        else:
            shname = am.alliance.shname
            allid = am.alliance.id

        try:
            rnkn[acc.id]
        except:
            RankingNone(None, shname, allid, acc.empire, acc.id, pts, 0).save()
        else:
            RankingNone(None, shname, allid, acc.empire, acc.id, pts, rnkn[acc.id] - nrid).save()

        nrid += 1
    

def regen_personal_ranking_mother():
    rnkn = ranking_against_ids(RankingMother.objects.all())
    ress = read_resources(Account.objects.all())
            # interchange this part
    score = []          # score is a list of tuples(accid, score)
    for accid, resdict in ress.iteritems():
        try:
            score.append((accid, resdict['mother'][0] + resdict['mother'][1] + resdict['mother'][2]))
        except:
            score.append((accid, 0))
            # score counting done
    score = sorted(score, key=lambda k: k[1], reverse=True)
    cursor = connection.cursor()
    cursor.execute("TRUNCATE TABLE stats_rankingmother")      # pwn the table

    nrid = 1
    for accid, pts in score:
        acc = Account.objects.get(id=accid)
        try:
            am = AllianceMembership.objects.get(account=acc)
        except:
            # not allied
            shname = ''
            allid = 0
        else:
            shname = am.alliance.shname
            allid = am.alliance.id

        try:
            rnkn[acc.id]
        except:
            RankingMother(None, shname, allid, acc.empire, acc.id, pts, 0).save()
        else:
            RankingMother(None, shname, allid, acc.empire, acc.id, pts, rnkn[acc.id] - nrid).save()

        nrid += 1


def regen_personal_ranking_army():
    rnkn = ranking_against_ids(RankingArmy.objects.all())
    ress = read_resources(Account.objects.all())
            # interchange this part
    score = []          # score is a list of tuples(accid, score)
    for accid, resdict in ress.iteritems():
        try:
            score.append((accid, resdict['landarmy'][0] + resdict['landarmy'][1] + resdict['landarmy'][2]))
        except:
            score.append((accid, 0))
            # score counting done
    score = sorted(score, key=lambda k: k[1], reverse=True)
    cursor = connection.cursor()
    cursor.execute("TRUNCATE TABLE stats_rankingarmy")      # pwn the table

    nrid = 1
    for accid, pts in score:
        acc = Account.objects.get(id=accid)
        try:
            am = AllianceMembership.objects.get(account=acc)
        except:
            # not allied
            shname = ''
            allid = 0
        else:
            shname = am.alliance.shname
            allid = am.alliance.id

        try:
            rnkn[acc.id]
        except:
            RankingArmy(None, shname, allid, acc.empire, acc.id, pts, 0).save()
        else:
            RankingArmy(None, shname, allid, acc.empire, acc.id, pts, rnkn[acc.id] - nrid).save()

        nrid += 1

def regen_personal_ranking():
    regen_personal_ranking_none()
    regen_personal_ranking_mother()
    regen_personal_ranking_army()


def regen_allied_ranking():
    alliances = Alliance.objects.all()
    # get amapt - dict(alliance_id => Alliance object)
    amapt = {}
    for alliance in alliances:
        amapt[alliance.id] = alliance
    # get rkrn - dict(alliance_id => current_position_on_list)
    rkrn = {}
    for ranking in RankingAlliance.objects.all():
        rkrn[ranking.alliance_id] = ranking.id
    # calculate score - dict(alliance_id => total_score)
    score = {}
    for alliance in alliances:
        alliance_sum = 0
        for ally in AllianceMembership.objects.filter(alliance=alliance):
            try:
                rxdict = eval(open(IGSTATISTICS+'rs'+str(ally.account_id), 'r').read())
            except:
                continue
            try:
                rxdict = rxdict[None][0] + rxdict[None][1] + rxdict[None][2]
            except:
                rxdict = 0
            alliance_sum += rxdict
        score[alliance.id] = alliance_sum
    # create pscore - list(tuple(alliance_id, score)
    pscore = []
    for allid, pts in score.iteritems():
        pscore.append((allid, pts))
    # sort pscore
    pscore = sorted(pscore, key=lambda k: k[1], reverse=True)
    cursor = connection.cursor()
    cursor.execute("TRUNCATE TABLE stats_rankingalliance")      # pwn the table

    nrid = 1
    for allid, pts in pscore:
        all = amapt[allid]
        try:
            rkrn[allid]
        except:
            RankingAlliance(None, all.shname, all.name, all.members, all.id, pts, 0).save()
        else:
            RankingAlliance(None, all.shname, all.name, all.members, all.id, pts, rkrn[allid]-nrid).save()
        nrid += 1    