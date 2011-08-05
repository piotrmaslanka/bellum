'''Inserts resource information to the template'''
from bellum.alliance.models import AllianceMembership

def plug_in(primaryguiobject):
    try:
        am = AllianceMembership.objects.get(account=primaryguiobject.account.id)
    except:
        primaryguiobject.registerObject('alliance', False)
    else:
        primaryguiobject.registerObject('alliance', am)


