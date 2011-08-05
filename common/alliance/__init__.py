from bellum.alliance.models import Alliance, AllianceMembership

def isAllied(account1, account2, alliance=None):
    if alliance == None:
        try:
            alliance = AllianceMembership.objects.get(account=account1).alliance
        except: # nie jestesmy w ogole w sojusz, wszyscy sa wrogami!
            return False

    try:
        if AllianceMembership.objects.get(account=account2).alliance == alliance:
            return True
        return False
    except:
        return False