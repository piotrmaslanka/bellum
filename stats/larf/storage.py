from bellum.stats import LARFDATABASE_ROOT
from datetime import datetime
import codecs

def fileFor(accid):
    try:
        return codecs.open(LARFDATABASE_ROOT+str(accid)+'.lif', 'r', 'utf-8')
    except:
        codecs.open(LARFDATABASE_ROOT+str(accid)+'.lif', 'w', 'utf-8')
        return codecs.open(LARFDATABASE_ROOT+str(accid)+'.lif', 'r', 'utf-8')


# 0.1 - newest
# 18.19 - oldest

def insertFor(accid, block):
    try:
        lst = map(lambda x: x[:-1], list(fileFor(accid).readlines())) # utnij ostatni
                                                        # znak - zawsze \n
    except:
        lst = []

    lst = [repr(datetime.now()), block] + lst
    w = codecs.open(LARFDATABASE_ROOT+str(accid)+'.lif', 'w', 'utf-8')

    if len(lst) > 20:
        lst = lst[:20]      # Cut the list

    for line in lst:
        w.write(line+u'\n')
    del w