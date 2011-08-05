from bellum.common.models import ResourceIndex
from bellum.stats import IGSTATISTICS as IPATH
from bellum.common.utils import SystemWideLock


def sumtuples(a, b):
    return a[0]+b[0], a[1]+b[1], a[2]+b[2]

#   Available:
#           mother, landarmy, research, province, scans, sent


def note(accid, rsobject, spendingcategory):
    swlock = SystemWideLock('igstatistics-resources_sent-note-'+str(accid)).acquire()

    try:
        fd = eval(open(IPATH+'rs'+str(accid), 'r').read())
    except:
        fd = {None: (0, 0, 0)}

    fd[None] = sumtuples(fd[None], (rsobject.titan, rsobject.pluton, rsobject.men))
    if spendingcategory <> None:
        try:
            fd[spendingcategory] = sumtuples(fd[spendingcategory], (rsobject.titan, rsobject.pluton, rsobject.men))
        except:
            fd[spendingcategory] = (rsobject.titan, rsobject.pluton, rsobject.men)

    open(IPATH+'rs'+str(accid), 'w').write(repr(fd))

    swlock.release()
