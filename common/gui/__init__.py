'''Preps GUI items for easy template display'''

from bellum.common.session.mother import getCurrentMother


from bellum.common.gui import resource_mod
from bellum.common.gui import my_mothers_mod
from bellum.common.gui import current_mother_mod
from bellum.common.gui import current_race_mod
from bellum.common.gui import account_mod
from bellum.common.gui import alliance_mod  # depends on account_mod

class PrimaryGUIObject(object):
    '''Is directly sent to template, embodies everything a GUI standard template object should have'''
    
    def __init__(self, request, mother=None):
        self._request = request
        if mother == None:
            self._mother = getCurrentMother(self._request)
        else:
            self._mother = mother
            
        # plugging in stuff
        
        resource_mod.plug_in(self)
        account_mod.plug_in(self)
        my_mothers_mod.plug_in(self)
        current_mother_mod.plug_in(self)
        current_race_mod.plug_in(self)
        alliance_mod.plug_in(self)

    def registerObject(self, name, obj):
        '''Registers a variable as self attribute'''
        self.__dict__[name] = obj
